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
	Fase 2: afhankelijkheden, fase-poort, scope-bewaking.
	"""
	enforce_group_for_work_type(doc)
	enforce_structure_rules(doc)
	set_span_ancestors(doc)
	enforce_dependencies(doc)
	enforce_phase_gate(doc)
	flag_meerwerk(doc)
	sync_board_state_to_status(doc)


# Bord-staten die "in uitvoering of verder" betekenen. Een taak mag hier pas
# komen als al haar depends_on-taken klaar (Done) of geannuleerd zijn.
ACTIVE_BOARD_STATES = {"Todo", "In Progress", "In Review", "Done"}
DONE_BOARD_STATES = {"Done", "Canceled"}


def enforce_dependencies(doc):
	"""Harde afhankelijkheid (fase 2): blokkeer het activeren van een taak
	zolang een van haar native depends_on-taken nog niet klaar is.

	'Activeren' = board_state naar Todo/In Progress/In Review/Done. Backlog
	blijft altijd toegestaan. Een depends_on-taak telt als klaar wanneer haar
	board_state Done of Canceled is (of, als die leeg is, status Completed/
	Cancelled). Zo dwingt het bord de volgorde af die de generator uitrolt.
	"""
	if doc.get("custom_board_state") not in ACTIVE_BOARD_STATES:
		return
	blocking = []
	for row in doc.get("depends_on") or []:
		dep = row.get("task")
		if not dep:
			continue
		state = frappe.db.get_value(
			"Task", dep, ["custom_board_state", "status", "subject"], as_dict=True
		)
		if not state:
			continue
		done = state.custom_board_state in DONE_BOARD_STATES or (
			not state.custom_board_state and state.status in ("Completed", "Cancelled")
		)
		if not done:
			blocking.append(state.subject or dep)
	if blocking:
		frappe.throw(
			_("Deze taak hangt af van werk dat nog niet klaar is: {0}.").format(
				", ".join(blocking)
			)
		)


def enforce_phase_gate(doc):
	"""Harde fase-poort (fase 2): een Phase-taak mag pas op Done als al haar
	onderliggende taken klaar zijn (Done/Canceled). De Doorgronden-fase vereist
	bovendien het Go-besluit op het Project (custom_decision == 'Go').

	De poort werkt op de Phase zelf: het bord laat een fase niet afsluiten
	terwijl er nog open werk onder hangt. Registers zijn aparte documenten en
	tellen niet mee.
	"""
	if doc.get("custom_work_type") != "Phase":
		return
	if doc.get("custom_board_state") != "Done":
		return

	# Doorgronden-poort = het Go/No-Go-beslismoment.
	if _is_doorgronden(doc) and doc.get("project"):
		decision = frappe.db.get_value("Project", doc.project, "custom_decision")
		if decision != "Go":
			frappe.throw(
				_(
					"De fase Doorgronden kan pas worden afgesloten nadat het "
					"Beslismoment op Go staat (Project-veld Decision)."
				)
			)

	open_children = _open_descendants(doc)
	if open_children:
		frappe.throw(
			_("Deze fase heeft nog open werk: {0}. Sluit dat eerst af.").format(
				", ".join(open_children[:5]) + ("..." if len(open_children) > 5 else "")
			)
		)


def _is_doorgronden(doc):
	subject = (doc.get("subject") or "").lower()
	return "doorgronden" in subject


def _open_descendants(doc):
	"""Subjects van niet-afgeronde nakomelingen via de NestedSet (lft/rgt)."""
	if not doc.get("lft") or not doc.get("rgt"):
		return []
	rows = frappe.get_all(
		"Task",
		filters={"lft": [">", doc.lft], "rgt": ["<", doc.rgt]},
		fields=["subject", "custom_board_state", "status", "is_group"],
	)
	out = []
	for r in rows:
		if r.is_group:
			continue
		done = r.custom_board_state in DONE_BOARD_STATES or (
			not r.custom_board_state and r.status in ("Completed", "Cancelled")
		)
		if not done:
			out.append(r.subject)
	return out


def flag_meerwerk(doc):
	"""Scope-bewaking (fase 2): een nieuw Epic/Story op een Go-project dat
	(nog) niet via een Requirement Link aan een geaccepteerde eis hangt, krijgt
	automatisch custom_meerwerk_status = 'Te beoordelen'.

	Zo wordt buiten-scope werk zichtbaar zonder het te blokkeren: een Projects
	Manager keurt het goed (Goedgekeurd) of parkeert het (Future project). De
	vlag wordt alleen gezet, nooit teruggedraaid (handmatig besluit wint).
	"""
	if doc.get("custom_work_type") not in ("Epic", "Story"):
		return
	if doc.get("custom_meerwerk_status"):
		return  # al beoordeeld of gemarkeerd; niet overschrijven
	if not doc.get("project"):
		return
	decision = frappe.db.get_value("Project", doc.project, "custom_decision")
	if decision != "Go":
		return  # scope-bewaking pas relevant na akkoord
	if not _has_accepted_requirement_link(doc):
		doc.custom_meerwerk_status = "To Review"


def _has_accepted_requirement_link(doc):
	"""True als deze taak via een Requirement Link aan een geaccepteerde eis
	hangt. Een nieuwe (ongesavede) taak heeft nog geen naam en dus geen links.
	"""
	if doc.get("__islocal") or not doc.get("name"):
		return False
	links = frappe.get_all(
		"Requirement Link",
		filters={"work_item": doc.name},
		fields=["requirement"],
	)
	for link in links:
		status = frappe.db.get_value("Requirement", link.requirement, "status")
		if status in ("Agreed", "Built", "Tested", "Accepted"):
			return True
	return False


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


@frappe.whitelist(methods=["POST"])
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


# ---------------------------------------------------------------------------
# Eis-status-roll (fase 2)
# De status van een eis volgt uit de dekking door stories/tests via Requirement
# Link. Keten: Draft -> Agreed -> Built -> Tested -> Accepted.
# - Draft:    geen enkele implements-link.
# - Agreed:   >=1 implements-link, maar nog niet alle implementerende taken Done.
# - Built:    alle implementerende taken Done (en er is er minstens 1).
# - Tested:   Built EN alle verifies-taken (tests) Done (en er is er minstens 1).
# - Accepted: handmatig eindbesluit; wordt door de roll nooit overschreven.
# Getriggerd vanuit Requirement Link-events en Task on_update.
# ---------------------------------------------------------------------------

def _build_done_map(task_names):
	"""Eén query: map elke taaknaam op done-ja/nee (board Done/Canceled, of
	als board leeg is status Completed/Cancelled). Vermijdt N+1."""
	done = {}
	names = list({t for t in task_names if t})
	if not names:
		return done
	for t in frappe.get_all(
		"Task",
		filters={"name": ["in", names]},
		fields=["name", "custom_board_state", "status"],
	):
		done[t.name] = t.custom_board_state in DONE_BOARD_STATES or (
			not t.custom_board_state and t.status in ("Completed", "Cancelled")
		)
	return done


def derive_requirement_status(requirement):
	"""Herbereken en schrijf de afgeleide status van een eis (idempotent).

	Respecteert het handmatige eindbesluit Accepted: een eis die op Accepted
	staat blijft staan. Schrijft via set_value zonder de eis opnieuw te
	valideren en zonder modified te bumpen (geen form-conflict bij open eis;
	afgeleide statussen worden bewust niet Version-gelogd).
	"""
	current = frappe.db.get_value("Requirement", requirement, "status")
	if current == "Accepted":
		return current

	links = frappe.get_all(
		"Requirement Link",
		filters={"requirement": requirement},
		fields=["work_item", "relation_type"],
	)
	implementers = [l.work_item for l in links if l.relation_type == "implements" and l.work_item]
	verifiers = [l.work_item for l in links if l.relation_type == "verifies" and l.work_item]

	done = _build_done_map(implementers + verifiers)

	if not implementers:
		# Geen implements-links: een handmatig opgehoogde Agreed blijft staan,
		# anders Draft. Built/Tested zonder implementers kan niet bestaan.
		new_status = "Agreed" if current == "Agreed" else "Draft"
	elif not all(done.get(t) for t in implementers):
		new_status = "Agreed"
	elif verifiers and all(done.get(t) for t in verifiers):
		new_status = "Tested"
	else:
		new_status = "Built"

	if new_status != current:
		frappe.db.set_value(
			"Requirement", requirement, "status", new_status, update_modified=False
		)
	return new_status


def requirement_link_changed(doc, method=None):
	"""doc_event op Requirement Link (on_update / after_delete): herbereken de
	status van de betrokken eis. after_delete (niet on_trash) zodat de query de
	zojuist verwijderde link niet meer meetelt."""
	if doc.get("requirement"):
		derive_requirement_status(doc.requirement)


def roll_requirements_for_task(doc, method=None):
	"""doc_event op Task (on_update): herbereken elke eis die via een
	Requirement Link aan deze taak hangt. Zo werkt het afronden van een story
	of test door naar de eis-status."""
	if doc.get("custom_work_type") not in ("Story", "Task", "Bug", "Epic"):
		return
	links = frappe.get_all(
		"Requirement Link", filters={"work_item": doc.name}, fields=["requirement"]
	)
	for link in {l.requirement for l in links if l.requirement}:
		derive_requirement_status(link)


# ---------------------------------------------------------------------------
# Tier-cancel (fase 2)
# Zodra het Project een tier krijgt (Basis/Plus/Premium), wordt werk met een
# hoger pakket dan de gekozen tier geannuleerd. De annulering loopt via een
# echte save zodat track_changes een Version vastlegt (audittrail van de scope).
# ---------------------------------------------------------------------------

TIER_RANK = {"Basis": 1, "Plus": 2, "Premium": 3, "Future": 4}


def project_tier_changed(doc, method=None):
	"""doc_event op Project (on_update): bij een gewijzigde tier het werk boven
	de tier annuleren. Alleen draaien als de tier daadwerkelijk veranderde."""
	before = doc.get_doc_before_save()
	new_tier = doc.get("custom_tier")
	if not new_tier:
		return
	if before and before.get("custom_tier") == new_tier:
		return
	cancel_work_above_tier(doc.name, new_tier)


def cancel_work_above_tier(project, tier):
	"""Annuleer alle (niet-group) taken van het project waarvan custom_package
	boven de gekozen tier ligt. Version-gelogd via doc.save()."""
	rank = TIER_RANK.get(tier)
	if not rank:
		return 0
	above = [pkg for pkg, r in TIER_RANK.items() if r > rank]
	if not above:
		return 0
	tasks = frappe.get_all(
		"Task",
		filters={
			"project": project,
			"custom_package": ["in", above],
			"is_group": 0,
			"custom_board_state": ["!=", "Canceled"],
		},
		pluck="name",
	)
	cancelled = 0
	for name in tasks:
		task = frappe.get_doc("Task", name)
		task.custom_board_state = "Canceled"
		task.save(ignore_permissions=True)
		cancelled += 1
	if cancelled:
		frappe.msgprint(
			_("{0} taak(en) buiten de tier {1} zijn geannuleerd.").format(cancelled, tier)
		)
	return cancelled


# ---------------------------------------------------------------------------
# Scope-document (fase 2)
# Levert de scope-data van een Project zodat het scope-document (Print Format
# "Span Scope Document") zichzelf vult uit de eisen-laag: bronnen, eisen per
# MoSCoW, dekking en het Go/No-Go-besluit. Geregistreerd als Jinja-method
# (zie hooks.py) zodat de zware queries in Python blijven, niet in de template.
# ---------------------------------------------------------------------------

MOSCOW_ORDER = ["Must", "Should", "Could", "Won't"]


def get_scope_data(project):
	"""Aggregeer de scope van een Project voor het scope-document.

	Geeft het project, de Requirement Sources (bronnen), de eisen gegroepeerd
	per MoSCoW, en de dekking (eisen zonder implements-link = scope-gaten).

	Toegangscontrole: deze method draait als Jinja-context (niet whitelisted),
	maar gebruikt frappe.get_all dat permissies omzeilt. Daarom een expliciete
	read-check op het Project, zodat de scope-data niet lekt aan iemand zonder
	leesrecht (ook niet via een eigen Print Format op een ander project).
	"""
	if not frappe.has_permission("Project", "read", project):
		frappe.throw(_("Niet toegestaan."), frappe.PermissionError)
	proj = frappe.db.get_value(
		"Project",
		project,
		["name", "project_name", "custom_tier", "custom_decision"],
		as_dict=True,
	)
	sources = frappe.get_all(
		"Requirement Source",
		filters={"project": project},
		fields=["source_id", "type", "title", "priority", "frequency", "description", "impact"],
		order_by="source_id asc",
	)
	reqs = frappe.get_all(
		"Requirement",
		filters={"project": project},
		fields=["name", "requirement_id", "title", "type", "priority", "status", "source"],
		order_by="requirement_id asc",
	)

	by_moscow = {k: [] for k in MOSCOW_ORDER}
	for r in reqs:
		by_moscow.setdefault(r.priority or "Must", []).append(r)

	req_names = [r.name for r in reqs]
	implemented = set()
	if req_names:
		for link in frappe.get_all(
			"Requirement Link",
			filters={"requirement": ["in", req_names], "relation_type": "implements"},
			fields=["requirement"],
		):
			implemented.add(link.requirement)
	gaps = [r for r in reqs if r.name not in implemented]

	return {
		"project": proj,
		"sources": sources,
		"moscow": [(k, by_moscow.get(k, [])) for k in MOSCOW_ORDER],
		"total": len(reqs),
		"gaps": gaps,
		"gap_count": len(gaps),
	}
