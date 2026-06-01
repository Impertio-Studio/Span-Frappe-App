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

# ---------------------------------------------------------------------------
# Per fase ingevuld. Zie span-startdocument.md (repo Span Frappe App workspace).
#
# Fase 1: fixtures = [Custom Field, Property Setter, Client Script, ...]
# Fase 3: doc_events = {"Task": {"validate": "span.api.sync_board_state"}}
# Fase 6: doc_events["Task"]["on_update"] = "span.api.check_phase_completion"
# Fase 7: span.billing.create_draft_invoice_for_phase()  (alleen docstatus=0)
# ---------------------------------------------------------------------------

# fixtures = []
# doc_events = {}
