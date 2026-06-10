"""Requirement Source (NL-weergave: Eis-bron): de herkomst van een eis.

Een generiek, getypeerd bron-doctype. Symmetrisch: elke herkomst is een
first-class record, ongeacht het type. Het klassieke knelpunt is gewoon een
Requirement Source met type=Problem (NL: Knelpunt), opgehaald uit het
Analyserapport. Een wens, risico of technische keuze is dezelfde structuur
met een ander type.

Per-project, per-type leesbare code via controller-autoname:
  Problem -> K-01, Wish -> W-01, Risk -> R-01, Technical -> T-01,
  Process -> P-01, System -> S-01, Data -> D-01, Role -> RO-01.
De docname is project-gekwalificeerd ("{project}-{source_id}").
"""

import frappe
from frappe import _
from frappe.model.document import Document

TYPE_PREFIX = {
	"Problem": "K",
	"Process": "P",
	"System": "S",
	"Data": "D",
	"Role": "RO",
	"Risk": "R",
	"Wish": "W",
	"Technical": "T",
}


class RequirementSource(Document):
	def autoname(self):
		if not self.project:
			frappe.throw(_("Een Requirement Source moet aan een Project gekoppeld zijn."))

		prefix = TYPE_PREFIX.get(self.type, "SRC")
		existing = frappe.get_all(
			"Requirement Source",
			filters={"project": self.project, "type": self.type},
			pluck="source_id",
		)
		next_seq = 1 + max(
			(int(sid.rsplit("-", 1)[1]) for sid in existing if sid),
			default=0,
		)
		self.source_id = f"{prefix}-{next_seq:02d}"
		self.name = f"{self.project}-{self.source_id}"
