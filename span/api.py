"""Span server-side logica (app-methode, geen RestrictedPython-sandbox).

Aangeroepen via doc_events in hooks.py. Imports zijn hier toegestaan,
in tegenstelling tot Server Scripts.
"""

import json
import os

import frappe
from frappe import _

# Werktypes die altijd een group-task (NestedSet-ouder) zijn.
GROUP_WORK_TYPES = {"Phase", "Step", "Epic"}

# Map skelet-type (uit span_skelet.json) -> custom_work_type op de Task.
# Poorten worden als gewone Task gemodelleerd (met een mijlpaal-prefix in de subject);
# registers zijn aparte documenten en worden NIET als taak uitgerold.
SKELET_TYPE_TO_WORK_TYPE = {"fase": "Phase", "step": "Step", "taak": "Task", "poort": "Task"}

# Eenrichtings mapping: het bord (custom_board_state) stuurt de native status.
# Overdue en Template staan hier bewust NIET in: Overdue beheert ERPNext zelf
# (op einddatum), en er is geen bord-kolom die ernaar mapt.
BOARD_STATE_TO_STATUS = {
	"Backlog": "Open",
	"Todo": "Open",
	"In Progress": "Working",
	"In Review": "Pending Review",
	"Done": "Completed",
	"Canceled": "Cancelled",
}


def task_validate(doc, method=None):
	"""Validate-handler op Task. Centraal punt voor alle Span-Task-logica.

	Draait via doc_events NA de ERPNext-controller-validate, dus de hier
	gezette status overschrijft die van ERPNext (gewenst voor de bord-sync).

	Fase 1: Phase/Epic worden group-tasks.
	Fase 3: board-state -> native status (eenrichting).
	Structuur: Phase onder Project, Step onder Phase.
	"""
	enforce_group_for_work_type(doc)
	enforce_structure_rules(doc)
	set_span_ancestors(doc)
	sync_board_state_to_status(doc)


def set_span_ancestors(doc):
	"""Vul custom_phase en custom_epic met de dichtstbijzijnde Phase- resp.
	Epic-voorouder. Maakt plat filteren mogelijk: 'alle werk onder Phase X'
	of 'Epic + bijbehorende stories', zonder de tree.
	"""
	phase = epic = None
	parent = doc.get("parent_task")
	seen = set()
	while parent and parent not in seen:
		seen.add(parent)
		row = frappe.db.get_value(
			"Task", parent, ["custom_work_type", "parent_task"], as_dict=True
		)
		if not row:
			break
		if row.custom_work_type == "Phase" and not phase:
			phase = parent
		if row.custom_work_type == "Epic" and not epic:
			epic = parent
		parent = row.parent_task
	doc.custom_phase = phase
	doc.custom_epic = epic


def enforce_structure_rules(doc):
	"""Twee bewuste structuurregels (verder is nesten vrij):

	- Een Phase hangt ALTIJD onder een Project (project-veld verplicht).
	- Een Step hangt ALTIJD onder een Phase (Phase als voorouder).

	Taken/Epics/Stories/Bugs mogen op elk niveau (Project/Phase/Step) los.
	"""
	work_type = doc.get("custom_work_type")
	if work_type == "Phase" and not doc.get("project"):
		frappe.throw(_("Een Phase moet onder een Project vallen: kies een Project."))
	if work_type == "Step" and not _has_phase_ancestor(doc):
		frappe.throw(_("Een Step moet onder een Phase vallen."))


def _has_phase_ancestor(doc):
	"""Loop de parent_task-keten omhoog tot een Phase of de top."""
	parent = doc.get("parent_task")
	seen = set()
	while parent and parent not in seen:
		seen.add(parent)
		row = frappe.db.get_value(
			"Task", parent, ["custom_work_type", "parent_task"], as_dict=True
		)
		if not row:
			break
		if row.custom_work_type == "Phase":
			return True
		parent = row.parent_task
	return False


def sync_board_state_to_status(doc):
	"""Map custom_board_state -> native status volgens BOARD_STATE_TO_STATUS.

	Eenrichting: het bord stuurt de status, nooit andersom. Alleen bij een
	gemapte board-state; anders blijft de bestaande status (incl. Overdue)
	ongemoeid. Uren raken de status hier nooit.
	"""
	target = BOARD_STATE_TO_STATUS.get(doc.get("custom_board_state"))
	if target and doc.status != target:
		doc.status = target


def enforce_group_for_work_type(doc):
	"""Zet is_group=1 wanneer het werktype een group-type is (Phase, Epic).

	Zet is_group nooit terug naar 0: de NestedSet blokkeert het ontgroepen
	van een task met kinderen, en niet-group-types mogen hun bestaande
	is_group behouden.
	"""
	if doc.get("custom_work_type") in GROUP_WORK_TYPES and not doc.is_group:
		doc.is_group = 1


# ---------------------------------------------------------------------------
# Structuur-generator (fase 2)
# Rolt het vaste Span-skelet (3 fases, hun steps, standaard-taken, poorten) uit
# op een Project. Hybride aanpak: dit is de Span-hook-engine; de trigger (een
# knop op het Project, of een Project Template) wordt erbovenop gezet.
# Bron = span/pm/span_skelet.json (gegenereerd uit de lean-analyse, single source).
# ---------------------------------------------------------------------------


def _load_span_skelet():
	"""Lees het standaard-skelet (depth-encoded rijen) uit de app."""
	path = os.path.join(frappe.get_app_path("span"), "pm", "span_skelet.json")
	with open(path, encoding="utf-8") as f:
		return json.load(f)


@frappe.whitelist()
def rollout_span_structure(project):
	"""Rol het standaard Span-skelet uit op een Project.

	- Idempotent: weigert als er al een Phase voor dit project bestaat (geen dubbele uitrol).
	- Registers (type 'register') worden NIET als taak aangemaakt: dat zijn aparte documenten.
	- Poorten worden als Task gemodelleerd met een mijlpaal-prefix in de subject.
	- De structuurregels (Phase onder Project, Step onder Phase) worden door task_validate
	  afgedwongen; daarom krijgt elke taak project + de juiste parent_task mee.
	"""
	if not project:
		frappe.throw(_("Project is verplicht."))
	if not frappe.has_permission("Project", "write", project):
		frappe.throw(_("Niet toegestaan."), frappe.PermissionError)
	if frappe.db.exists("Task", {"project": project, "custom_work_type": "Phase"}):
		frappe.throw(_("De Span-structuur is al uitgerold op dit project."))

	skelet = _load_span_skelet()
	parent_by_depth = {}
	created = 0
	skipped_registers = 0

	for row in skelet:
		depth = row["depth"]
		ntype = row["type"]
		name = row["name"]
		desc = row.get("desc") or None

		if ntype == "register":
			skipped_registers += 1
			continue

		work_type = SKELET_TYPE_TO_WORK_TYPE.get(ntype, "Task")
		subject = f"◆ {name}" if ntype == "poort" else name
		parent = parent_by_depth.get(depth - 1)

		task = frappe.get_doc(
			{
				"doctype": "Task",
				"subject": subject,
				"project": project,
				"parent_task": parent,
				"custom_work_type": work_type,
				"custom_board_state": "Backlog",
				"description": desc,
			}
		)
		task.insert(ignore_permissions=True)

		# Onthoud deze node als ouder voor diepere rijen; ruim diepere niveaus op.
		parent_by_depth[depth] = task.name
		for d in [d for d in parent_by_depth if d > depth]:
			del parent_by_depth[d]
		created += 1

	return {
		"project": project,
		"created": created,
		"skipped_registers": skipped_registers,
	}
