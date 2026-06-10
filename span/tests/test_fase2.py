"""Integratietests voor de Span fase-2 server-logica (span/api.py).

Dekt de keten die via doc_events loopt: structuurregels, harde
afhankelijkheden, fase-poort + Beslismoment, scope-bewaking (meerwerk),
eis-status-roll en tier-cancel. Draait tegen een testsite met de PM-fixtures
geladen (de custom fields moeten bestaan).

Run: bench --site <site> run-tests --module span.tests.test_fase2
"""

import frappe
from frappe.tests.classes import IntegrationTestCase


def _project(name, tier=None, decision="Pending"):
	doc = frappe.get_doc({
		"doctype": "Project",
		"project_name": name,
		"custom_decision": decision,
	})
	if tier:
		doc.custom_tier = tier
	doc.insert(ignore_permissions=True)
	return doc


def _task(subject, **kwargs):
	doc = frappe.get_doc({"doctype": "Task", "subject": subject, **kwargs})
	doc.insert(ignore_permissions=True)
	return doc


def _requirement(title, project, rtype="Functional", priority="Must"):
	doc = frappe.get_doc({
		"doctype": "Requirement",
		"title": title,
		"type": rtype,
		"priority": priority,
		"project": project,
	})
	doc.insert(ignore_permissions=True)
	return doc


def _link(requirement, work_item, relation_type):
	doc = frappe.get_doc({
		"doctype": "Requirement Link",
		"requirement": requirement,
		"work_item": work_item,
		"relation_type": relation_type,
	})
	doc.insert(ignore_permissions=True)
	return doc


class TestSpanStructure(IntegrationTestCase):
	def test_phase_becomes_group_and_needs_project(self):
		project = _project("_Test Span Structure")
		phase = _task("_Test Phase", custom_work_type="Phase", project=project.name)
		self.assertEqual(phase.is_group, 1)

	def test_phase_without_project_throws(self):
		self.assertRaises(
			frappe.ValidationError,
			_task,
			"_Test Phase No Project",
			custom_work_type="Phase",
		)

	def test_step_without_phase_ancestor_throws(self):
		project = _project("_Test Span Step")
		self.assertRaises(
			frappe.ValidationError,
			_task,
			"_Test Loose Step",
			custom_work_type="Step",
			project=project.name,
		)


class TestSpanDependencies(IntegrationTestCase):
	def test_dependency_blocks_activation(self):
		project = _project("_Test Span Deps")
		blocker = _task("_Test Blocker", project=project.name, custom_board_state="Backlog")
		dependent = _task("_Test Dependent", project=project.name, custom_board_state="Backlog")
		dependent.append("depends_on", {"task": blocker.name})
		dependent.save(ignore_permissions=True)

		dependent.custom_board_state = "In Progress"
		self.assertRaises(frappe.ValidationError, dependent.save, ignore_permissions=True)

	def test_dependency_allows_when_done(self):
		project = _project("_Test Span Deps OK")
		blocker = _task("_Test Blocker OK", project=project.name, custom_board_state="Done")
		dependent = _task("_Test Dependent OK", project=project.name, custom_board_state="Backlog")
		dependent.append("depends_on", {"task": blocker.name})
		dependent.save(ignore_permissions=True)

		dependent.custom_board_state = "In Progress"
		dependent.save(ignore_permissions=True)  # mag niet throwen
		self.assertEqual(dependent.custom_board_state, "In Progress")


class TestSpanPhaseGate(IntegrationTestCase):
	def test_phase_done_blocked_by_open_child(self):
		project = _project("_Test Span Gate", decision="Go")
		phase = _task("_Test Realiseren", custom_work_type="Phase", project=project.name)
		_task("_Test Open Child", project=project.name, parent_task=phase.name,
		      custom_board_state="Backlog")

		phase.reload()
		phase.custom_board_state = "Done"
		self.assertRaises(frappe.ValidationError, phase.save, ignore_permissions=True)

	def test_phase_done_allowed_when_children_done(self):
		project = _project("_Test Span Gate OK", decision="Go")
		phase = _task("_Test Realiseren OK", custom_work_type="Phase", project=project.name)
		_task("_Test Done Child", project=project.name, parent_task=phase.name,
		      custom_board_state="Done")

		phase.reload()
		phase.custom_board_state = "Done"
		phase.save(ignore_permissions=True)
		self.assertEqual(phase.custom_board_state, "Done")

	def test_doorgronden_requires_go(self):
		project = _project("_Test Span Doorgronden", decision="Pending")
		phase = _task("_Test Doorgronden", custom_work_type="Phase", project=project.name)

		phase.reload()
		phase.custom_board_state = "Done"
		self.assertRaises(frappe.ValidationError, phase.save, ignore_permissions=True)

		frappe.db.set_value("Project", project.name, "custom_decision", "Go")
		phase.reload()
		phase.custom_board_state = "Done"
		phase.save(ignore_permissions=True)  # met Go mag het
		self.assertEqual(phase.custom_board_state, "Done")


class TestSpanMeerwerk(IntegrationTestCase):
	def test_story_on_go_project_flagged_to_review(self):
		project = _project("_Test Span Meerwerk", decision="Go")
		story = _task("_Test Loose Story", custom_work_type="Story", project=project.name)
		self.assertEqual(story.custom_meerwerk_status, "To Review")

	def test_story_on_pending_project_not_flagged(self):
		project = _project("_Test Span No Flag", decision="Pending")
		story = _task("_Test Story Pending", custom_work_type="Story", project=project.name)
		self.assertFalse(story.custom_meerwerk_status)


class TestSpanRequirementRoll(IntegrationTestCase):
	def test_status_rolls_from_links(self):
		project = _project("_Test Span Roll")
		req = _requirement("_Test Eis", project.name)
		story = _task("_Test Impl Story", custom_work_type="Story", project=project.name,
		              custom_board_state="Backlog")
		_link(req.name, story.name, "implements")

		# 1 implements-link, story niet done -> Agreed
		self.assertEqual(frappe.db.get_value("Requirement", req.name, "status"), "Agreed")

		# story done -> Built
		story.custom_board_state = "Done"
		story.save(ignore_permissions=True)
		self.assertEqual(frappe.db.get_value("Requirement", req.name, "status"), "Built")

		# verifies-test done -> Tested
		test = _task("_Test UAT", custom_work_type="Task", project=project.name,
		             custom_board_state="Done")
		_link(req.name, test.name, "verifies")
		self.assertEqual(frappe.db.get_value("Requirement", req.name, "status"), "Tested")


class TestSpanTierCancel(IntegrationTestCase):
	def test_work_above_tier_cancelled(self):
		# De tier-cancel draait via project_tier_changed als achtergrondjob
		# (frappe.enqueue, enqueue_after_commit). In een test wordt niet
		# gecommit, dus toetsen we de jobfunctie cancel_work_above_tier direct.
		from span.api import cancel_work_above_tier

		project = _project("_Test Span Tier")
		premium = _task("_Test Premium Work", project=project.name,
		                custom_package="Premium", custom_board_state="Todo")
		basis = _task("_Test Basis Work", project=project.name,
		              custom_package="Basis", custom_board_state="Todo")

		cancelled = cancel_work_above_tier(project.name, "Basis")

		self.assertEqual(cancelled, 1)
		self.assertEqual(
			frappe.db.get_value("Task", premium.name, "custom_board_state"), "Canceled"
		)
		self.assertEqual(
			frappe.db.get_value("Task", basis.name, "custom_board_state"), "Todo"
		)
