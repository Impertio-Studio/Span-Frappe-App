"""Span server-side logica (app-methode, geen RestrictedPython-sandbox).

Aangeroepen via doc_events in hooks.py. Imports zijn hier toegestaan,
in tegenstelling tot Server Scripts.
"""

import frappe

# Werktypes die altijd een group-task (NestedSet-ouder) zijn.
GROUP_WORK_TYPES = {"Phase", "Epic"}

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
	"""
	enforce_group_for_work_type(doc)
	sync_board_state_to_status(doc)


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
