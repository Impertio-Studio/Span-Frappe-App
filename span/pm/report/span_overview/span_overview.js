// Span Overview — filters
frappe.query_reports["Span Overview"] = {
	filters: [
		{
			fieldname: "project",
			label: __("Project"),
			fieldtype: "Link",
			options: "Project",
		},
	],
};
