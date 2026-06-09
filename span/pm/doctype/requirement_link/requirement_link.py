"""Requirement Link: junction tussen een eis en een werk-item.

Lees een rij als een zin: "Story X implements F-01". Maakt many-to-many
mogelijk (een eis aan veel stories en omgekeerd) en draagt zelf betekenis
via relation_type (implements / verifies / depends-on).
"""

import frappe
from frappe.model.document import Document


class RequirementLink(Document):
	pass
