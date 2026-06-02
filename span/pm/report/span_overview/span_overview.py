"""Span Overview — rollup per Phase/Epic over de NestedSet-descendants.

Per group-task (Phase/Epic): aantal werk-items, % done, story points,
geschat vs werkelijk uren, open items. Eenvoudige technische-PM-rollup,
geen budget/facturatie.
"""

import frappe
from frappe import _

GROUP_TYPES = ("Phase", "Epic")


def execute(filters=None):
	filters = filters or {}
	data = get_data(filters)
	return get_columns(), data, None, get_chart(data), get_summary(data)


def get_columns():
	return [
		{"fieldname": "work_type", "label": _("Type"), "fieldtype": "Data", "width": 80},
		{"fieldname": "name", "label": _("Task"), "fieldtype": "Link", "options": "Task", "width": 150},
		{"fieldname": "subject", "label": _("Subject"), "fieldtype": "Data", "width": 240},
		{"fieldname": "board_state", "label": _("Board"), "fieldtype": "Data", "width": 110},
		{"fieldname": "status", "label": _("Status"), "fieldtype": "Data", "width": 110},
		{"fieldname": "children", "label": _("Items"), "fieldtype": "Int", "width": 70},
		{"fieldname": "percent_done", "label": _("% Done"), "fieldtype": "Percent", "width": 90},
		{"fieldname": "story_points", "label": _("Points"), "fieldtype": "Int", "width": 70},
		{"fieldname": "est_hours", "label": _("Est. h"), "fieldtype": "Float", "width": 80},
		{"fieldname": "actual_hours", "label": _("Actual h"), "fieldtype": "Float", "width": 80},
		{"fieldname": "open_items", "label": _("Open"), "fieldtype": "Int", "width": 70},
	]


def get_data(filters):
	group_filters = {"custom_work_type": ["in", GROUP_TYPES]}
	if filters.get("project"):
		group_filters["project"] = filters["project"]

	groups = frappe.get_all(
		"Task",
		filters=group_filters,
		fields=[
			"name", "subject", "custom_work_type", "custom_board_state",
			"status", "lft", "rgt",
		],
		order_by="lft asc",
	)

	rows = []
	for g in groups:
		agg = frappe.db.sql(
			"""
			SELECT
				COUNT(*) AS children,
				SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) AS done,
				SUM(CASE WHEN status NOT IN ('Completed', 'Cancelled') THEN 1 ELSE 0 END) AS open_items,
				COALESCE(SUM(custom_story_points), 0) AS story_points,
				COALESCE(SUM(expected_time), 0) AS est_hours,
				COALESCE(SUM(actual_time), 0) AS actual_hours
			FROM `tabTask`
			WHERE lft > %(lft)s AND rgt < %(rgt)s AND is_group = 0
			""",
			{"lft": g.lft, "rgt": g.rgt},
			as_dict=True,
		)[0]

		children = agg.children or 0
		done = agg.done or 0
		rows.append({
			"work_type": g.custom_work_type,
			"name": g.name,
			"subject": g.subject,
			"board_state": g.custom_board_state,
			"status": g.status,
			"children": children,
			"percent_done": (done / children * 100) if children else 0,
			"story_points": agg.story_points or 0,
			"est_hours": agg.est_hours or 0,
			"actual_hours": agg.actual_hours or 0,
			"open_items": agg.open_items or 0,
		})
	return rows


def get_chart(data):
	rows = [d for d in data if d["children"]][:12]
	return {
		"data": {
			"labels": [d["subject"][:24] for d in rows],
			"datasets": [{"name": _("% Done"), "values": [round(d["percent_done"], 1) for d in rows]}],
		},
		"type": "percentage",
		"height": 240,
	}


def get_summary(data):
	total_open = sum(d["open_items"] for d in data)
	est = sum(d["est_hours"] for d in data)
	actual = sum(d["actual_hours"] for d in data)
	return [
		{"value": len(data), "label": _("Phases/Epics"), "datatype": "Int", "indicator": "Blue"},
		{"value": total_open, "label": _("Open items"), "datatype": "Int",
		 "indicator": "Orange" if total_open else "Green"},
		{"value": est, "label": _("Estimated h"), "datatype": "Float", "indicator": "Grey"},
		{"value": actual, "label": _("Actual h"), "datatype": "Float",
		 "indicator": "Red" if actual > est else "Green"},
	]
