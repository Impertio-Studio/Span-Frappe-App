// Span: knop op het Project om het standaard-skelet uit te rollen.
// Roept span.api.rollout_span_structure aan (idempotent; weigert bij dubbele uitrol).
frappe.ui.form.on("Project", {
	refresh(frm) {
		if (frm.is_new()) return;
		frm.add_custom_button(
			__("Structuur uitrollen"),
			() => {
				frappe.confirm(
					__("Het standaard Span-skelet (fases, stappen, taken, poorten) uitrollen op dit project?"),
					() => {
						frappe.call({
							method: "span.api.rollout_span_structure",
							args: { project: frm.doc.name },
							freeze: true,
							freeze_message: __("Structuur uitrollen..."),
							callback(r) {
								if (r.message) {
									frappe.msgprint(
										__("Span-structuur uitgerold: {0} taken aangemaakt.", [
											r.message.created,
										])
									);
									frm.reload_doc();
								}
							},
						});
					}
				);
			},
			__("Span")
		);
	},
});
