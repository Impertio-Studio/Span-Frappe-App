"""Requirement: de eis als contract (het 'wat'), los van de werkboom.

Per-project leesbare code via controller-autoname:
  Functional      -> F-01, F-02, ...
  Non-Functional  -> NFR-01, NFR-02, ...

De docname is project-gekwalificeerd ("{project}-{requirement_id}") zodat hij
globaal uniek blijft terwijl requirement_id per project opnieuw bij 1 begint.
"""

import frappe
from frappe import _
from frappe.model.document import Document


class Requirement(Document):
	def autoname(self):
		if not self.project:
			frappe.throw(_("Een Requirement moet aan een Project gekoppeld zijn."))

		abbr = "NFR" if self.type == "Non-Functional" else "F"
		existing = frappe.get_all(
			"Requirement",
			filters={"project": self.project, "type": self.type},
			pluck="requirement_id",
		)
		next_seq = 1 + max(
			(int(rid.rsplit("-", 1)[1]) for rid in existing if rid),
			default=0,
		)
		self.requirement_id = f"{abbr}-{next_seq:02d}"
		self.name = f"{self.project}-{self.requirement_id}"
