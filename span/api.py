"""Span server-side logica (app-methode, geen RestrictedPython-sandbox).

Aangeroepen via doc_events in hooks.py. Imports zijn hier toegestaan,
in tegenstelling tot Server Scripts.
"""

import frappe

# Werktypes die altijd een group-task (NestedSet-ouder) zijn.
GROUP_WORK_TYPES = {"Phase", "Epic"}


def task_validate(doc, method=None):
	"""Validate-handler op Task. Centraal punt voor alle Span-Task-logica.

	Fase 1: Phase/Epic worden group-tasks.
	Fase 3 breidt dit uit met board-state -> status sync.
	"""
	enforce_group_for_work_type(doc)


def enforce_group_for_work_type(doc):
	"""Zet is_group=1 wanneer het werktype een group-type is (Phase, Epic).

	Zet is_group nooit terug naar 0: de NestedSet blokkeert het ontgroepen
	van een task met kinderen, en niet-group-types mogen hun bestaande
	is_group behouden.
	"""
	if doc.get("custom_work_type") in GROUP_WORK_TYPES and not doc.is_group:
		doc.is_group = 1
