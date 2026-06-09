"""Pain Point (NL-weergave: Knelpunt): een pijnpunt, risico of probleem in de
huidige werkwijze van de klant. Opgehaald in Fase 1 (Doorgronden), vormt de
bron van eisen.

Per-project leesbare code via controller-autoname: PP-01, PP-02, ...
De docname is project-gekwalificeerd ("{project}-{pain_point_id}") zodat hij
globaal uniek blijft terwijl pain_point_id per project opnieuw bij 1 begint.
"""

import frappe
from frappe import _
from frappe.model.document import Document


class PainPoint(Document):
	def autoname(self):
		if not self.project:
			frappe.throw(_("Een Pain Point moet aan een Project gekoppeld zijn."))

		existing = frappe.get_all(
			"Pain Point",
			filters={"project": self.project},
			pluck="pain_point_id",
		)
		next_seq = 1 + max(
			(int(pid.rsplit("-", 1)[1]) for pid in existing if pid),
			default=0,
		)
		self.pain_point_id = f"PP-{next_seq:02d}"
		self.name = f"{self.project}-{self.pain_point_id}"
