// Task form: snel een Requirement Link leggen vanuit een werk-item.
// Voor de scope-workflow: een story die op "To Review" staat wordt
// goedgekeurd zodra hij via een implements-link aan een eis hangt.
frappe.ui.form.on("Task", {
	refresh(frm) {
		if (frm.is_new()) return;
		frm.add_custom_button(
			__("Link Requirement"),
			() => {
				frappe.new_doc("Requirement Link", {
					work_item: frm.doc.name,
					relation_type: "implements",
				});
			},
			__("Span"),
		);
	},
});
