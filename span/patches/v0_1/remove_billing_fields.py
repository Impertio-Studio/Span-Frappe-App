"""Scope-herijking 2026-06-02: billing valt buiten Span.

Verwijdert de drie billing-only Custom Fields op Task die in Fase 1 zijn
aangemaakt. Idempotent: alleen verwijderen wat bestaat.
"""

import frappe

BILLING_FIELDS = ("custom_phase_amount", "custom_so_item", "custom_invoiced")


def execute():
	for fieldname in BILLING_FIELDS:
		name = f"Task-{fieldname}"
		if frappe.db.exists("Custom Field", name):
			frappe.delete_doc("Custom Field", name, ignore_permissions=True)
	frappe.clear_cache(doctype="Task")
