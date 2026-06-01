# Span

Agile projectmanagement native in ERPNext. Span voegt een gelaagde werkstructuur (Project, Phase, Epic, Story, Task, Bug) en fase-gestuurde facturatie toe, zonder core-wijzigingen aan Frappe of ERPNext.

## Versie

**Doelversie: ERPNext / Frappe v16.** De app wordt tegen v16 gebouwd en getest. Installeer niet op v14 of v15 zonder aanpassing van `pyproject.toml`.

## Wat Span doet

- Werktype op `Task` via `custom_work_type` (Phase, Epic, Story, Task, Bug). Phase en Epic zijn group-tasks.
- Hierarchie via de native `parent_task` NestedSet: Project, Phase, Epic, Story/Bug/Task, subtaak.
- Kanban-bordlaag (`custom_board_state`) die eenrichtings synct naar de native `status`.
- Project Template met vaste fases en bedragen als startpunt voor een Sales Order.
- Concept-facturatie per afgeronde fase (altijd draft, nooit definitief, idempotent).

Volledige specificatie en bouwroadmap: zie het technische startdocument in de Span-workspace (`span-startdocument.md`).

## Installatie

Span is een standaard Frappe-app. Op een bench met ERPNext v16:

```bash
# clone als app "span" (repo-naam wijkt af, daarom expliciet de app-naam meegeven)
bench get-app span https://github.com/Impertio-Studio/Span-Frappe-App.git

# installeer op een site
bench --site <site> install-app span

# schema en fixtures toepassen
bench --site <site> migrate
```

Test eerst op een wegwerp-site. Facturatie-functionaliteit (latere fase) raakt echte Sales Orders en Sales Invoices: draai die uitsluitend na expliciete bevestiging op een live boekhouding.

## Ontwikkeling

Span wordt gebouwd met het Frappe_Claude_Skill_Package (Impertio Studio). Laad voor elke taak de relevante skill (de triade `syntax` + `impl` + `errors`). Server Scripts draaien in een RestrictedPython-sandbox: gebruik altijd de `frappe.*`-namespace, nooit `import`.

## Licentie

MIT. Zie `license.txt`.
