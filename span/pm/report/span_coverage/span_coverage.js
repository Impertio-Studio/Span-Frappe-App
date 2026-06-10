// Span Coverage — filters
frappe.query_reports["Span Coverage"] = {
	filters: [
		{
			fieldname: "project",
			label: __("Project"),
			fieldtype: "Link",
			options: "Project",
		},
	],
};
