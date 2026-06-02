// Span — Task list view: kleur de rij-indicator op custom_board_state,
// consistent met de Span Board kanban-kolommen.
frappe.listview_settings["Task"] = Object.assign(
	frappe.listview_settings["Task"] || {},
	{
		add_fields: ["custom_board_state", "custom_work_type", "is_group"],

		get_indicator(doc) {
			const colors = {
				Backlog: "gray",
				Todo: "light-blue",
				"In Progress": "orange",
				"In Review": "purple",
				Done: "green",
				Canceled: "red",
			};
			const state = doc.custom_board_state;
			if (state && colors[state]) {
				return [__(state), colors[state], "custom_board_state,=," + state];
			}
			// Geen board-state gezet: laat de native status-indicator met rust.
			return undefined;
		},
	}
);
