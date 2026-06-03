app_name = "span"
app_title = "Span"
app_publisher = "Impertio Studio"
app_description = (
	"Agile projectmanagement (Project, Phase, Epic, Story, Task, Bug) "
	"en fase-gestuurde facturatie, native in ERPNext v16."
)
app_email = "dev@impertio.nl"
app_license = "mit"

# Span bouwt voort op ERPNext (Task, Project, Sales Order, Sales Invoice).
required_apps = ["frappe", "erpnext"]

# Span als app-tegel in de Desk apps-launcher (/apps) -> opent de Span PM-workspace.
add_to_apps_screen = [
	{
		"name": "span",
		"logo": "/assets/span/images/span-logo.svg",
		"title": "Span",
		"route": "/app/span-pm",
	}
]

# ---------------------------------------------------------------------------
# Fixtures: alles wat een schone site via `migrate` moet reproduceren.
# Fase 1: 3 Custom Fields op Task (work_type, board_state, story_points).
# Fase 2: Kanban Board "Span Board" (Task op custom_board_state).
# Fase 5: Workspace "Span PM" (bundelt board, overview-report, taken).
# (Het Span Overview-report synct als standard report uit pm/report/.)
# ---------------------------------------------------------------------------
fixtures = [
	{"dt": "Custom Field", "filters": [["module", "=", "PM"]]},
	{"dt": "Property Setter", "filters": [["module", "=", "PM"]]},
	{"dt": "Span Discipline"},
	{"dt": "Kanban Board", "filters": [["name", "in", ["Span Board"]]]},
]
# Workspace "Span PM" komt uit de module-map pm/workspace/span_pm/ (standaard
# workspace), NIET via fixtures: Frappe verwijdert publieke fixture-workspaces
# als "orphan" tijdens migrate.

# Task list view: board-state-gekleurde indicatoren (Fase 2).
doctype_list_js = {"Task": "public/js/task_list.js"}

# ---------------------------------------------------------------------------
# Document-events (app-methode, imports toegestaan; geen Server Script-sandbox).
# Fase 1: Phase/Epic -> is_group via task_validate.
# Fase 3 breidt task_validate uit met board-state -> status sync.
# Fase 6 voegt on_update toe (span.api.check_phase_completion).
# ---------------------------------------------------------------------------
doc_events = {
	"Task": {
		"validate": "span.api.task_validate",
	},
}
