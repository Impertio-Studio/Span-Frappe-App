"""Span Coverage — the coverage report (phase 2).

Closes the chain: makes visible whether every requirement is covered by work.
Per requirement: how many implementing stories and verifying tests are linked,
how many of those are done, and a coverage verdict. A requirement without an
implements-link is a scope gap (nothing is being built for it). The other side
(a story without a requirement link = extra work) lives on the Task list via
custom_meerwerk_status.

No budget or billing; purely traceability from requirement to built/tested.
"""

import frappe
from frappe import _

DONE_BOARD_STATES = ("Done", "Canceled")

# Coverage verdict -> cell colour indicator.
COVERAGE_INDICATOR = {
	"Scope Gap": "Red",
	"Incomplete": "Orange",
	"Built": "Blue",
	"Tested": "Green",
	"Accepted": "Green",
}


def execute(filters=None):
	filters = filters or {}
	data = get_data(filters)
	return get_columns(), data, None, get_chart(data), get_summary(data)


def get_columns():
	return [
		{"fieldname": "name", "label": _("Requirement"), "fieldtype": "Link", "options": "Requirement", "width": 150},
		{"fieldname": "title", "label": _("Title"), "fieldtype": "Data", "width": 240},
		{"fieldname": "type", "label": _("Type"), "fieldtype": "Data", "width": 110},
		{"fieldname": "priority", "label": _("MoSCoW"), "fieldtype": "Data", "width": 90},
		{"fieldname": "status", "label": _("Status"), "fieldtype": "Data", "width": 100},
		{"fieldname": "implementers", "label": _("Stories"), "fieldtype": "Int", "width": 80},
		{"fieldname": "implementers_done", "label": _("Story done"), "fieldtype": "Int", "width": 90},
		{"fieldname": "verifiers", "label": _("Tests"), "fieldtype": "Int", "width": 80},
		{"fieldname": "verifiers_done", "label": _("Test done"), "fieldtype": "Int", "width": 90},
		{"fieldname": "coverage", "label": _("Coverage"), "fieldtype": "Data", "width": 120},
	]


def get_data(filters):
	req_filters = {}
	if filters.get("project"):
		req_filters["project"] = filters["project"]

	requirements = frappe.get_all(
		"Requirement",
		filters=req_filters,
		fields=["name", "title", "type", "priority", "status"],
		order_by="priority asc, name asc",
	)

	# All links for these requirements in one query, then grouped in Python.
	req_names = [r.name for r in requirements]
	links = []
	if req_names:
		links = frappe.get_all(
			"Requirement Link",
			filters={"requirement": ["in", req_names]},
			fields=["requirement", "work_item", "relation_type"],
		)

	# work_item -> done? in one lookup.
	work_items = list({l.work_item for l in links if l.work_item})
	done_map = {}
	if work_items:
		for t in frappe.get_all(
			"Task",
			filters={"name": ["in", work_items]},
			fields=["name", "custom_board_state", "status"],
		):
			done_map[t.name] = t.custom_board_state in DONE_BOARD_STATES or (
				not t.custom_board_state and t.status in ("Completed", "Cancelled")
			)

	by_req = {}
	for l in links:
		by_req.setdefault(l.requirement, {"impl": [], "verif": []})
		if l.relation_type == "implements" and l.work_item:
			by_req[l.requirement]["impl"].append(l.work_item)
		elif l.relation_type == "verifies" and l.work_item:
			by_req[l.requirement]["verif"].append(l.work_item)

	rows = []
	for r in requirements:
		grp = by_req.get(r.name, {"impl": [], "verif": []})
		impl, verif = grp["impl"], grp["verif"]
		impl_done = sum(1 for t in impl if done_map.get(t))
		verif_done = sum(1 for t in verif if done_map.get(t))
		rows.append({
			"name": r.name,
			"title": r.title,
			"type": r.type,
			"priority": r.priority,
			"status": r.status,
			"implementers": len(impl),
			"implementers_done": impl_done,
			"verifiers": len(verif),
			"verifiers_done": verif_done,
			"coverage": _coverage_verdict(r.status, impl, impl_done, verif, verif_done),
		})
	return rows


def _coverage_verdict(status, impl, impl_done, verif, verif_done):
	if status == "Accepted":
		return "Accepted"
	if not impl:
		return "Scope Gap"
	if impl_done < len(impl):
		return "Incomplete"
	if verif and verif_done == len(verif):
		return "Tested"
	return "Built"


def get_chart(data):
	buckets = {}
	for d in data:
		buckets[d["coverage"]] = buckets.get(d["coverage"], 0) + 1
	labels = [k for k in COVERAGE_INDICATOR if k in buckets]
	return {
		"data": {
			"labels": labels,
			"datasets": [{"name": _("Requirements"), "values": [buckets[k] for k in labels]}],
		},
		"type": "bar",
		"height": 240,
	}


def get_summary(data):
	gaps = sum(1 for d in data if d["coverage"] == "Scope Gap")
	tested = sum(1 for d in data if d["coverage"] in ("Tested", "Accepted"))
	total = len(data)
	return [
		{"value": total, "label": _("Requirements"), "datatype": "Int", "indicator": "Blue"},
		{"value": gaps, "label": _("Scope gaps"), "datatype": "Int",
		 "indicator": "Red" if gaps else "Green"},
		{"value": tested, "label": _("Tested/Accepted"), "datatype": "Int",
		 "indicator": "Green"},
		{"value": f"{round(tested / total * 100) if total else 0}%",
		 "label": _("Coverage rate"), "datatype": "Data",
		 "indicator": "Green" if total and tested == total else "Orange"},
	]
