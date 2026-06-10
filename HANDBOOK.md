# Span: Instruction Handbook

> Handboek voor de Span Frappe-app: agile projectmanagement native in ERPNext v16. Geschikt voor mensen én AI-agents. Markeert overal wat **[GEBOUWD]** is versus **[GEPLAND]** (besloten ontwerp, nog te bouwen).
>
> Bron van waarheid voor het ontwerp is het levende beslissingsdocument `Span-Architectuur-en-Beslissingen.html` (in de workspace-root en in `Infographics/Pitches/Onze werkwijze/`). Dit handboek loopt daarmee mee.

**Status:** concept v0.1, gegenereerd via agent-team.

## Inhoud
- A. Overzicht, methodiek en werkhierarchie
- B. Datamodel en doctypes (gebouwd + gepland)
- C. Gebruik (mensen in de Desk, en AI/agents)
- Roadmap / bouwlijst
- Onderhoud van dit handboek

---

## Sectie A: Fundament

---

## A.1 Wat is Span

Span is een Frappe-app die agile projectmanagement native toevoegt aan ERPNext v16. De app voegt een gestructureerde werk-boom (Project, Phase, Step, Epic, Story, Bug, Task), een eisen-catalogus (Requirement) en een koppelingslaag (Requirement Link) toe aan ERPNext, zodat de volledige uitvoeringscyclus van een IT-project, van intake tot go-live, op één plek beheerd wordt. Span introduceert geen aparte omgeving: alles draait binnen de bestaande ERPNext-installatie en maakt gebruik van native doctypes (Project, Task) uitgebreid met custom fields en eigen doctypes. De datalaag gebruikt Engelse keys; de weergave aan de gebruiker volgt de ingestelde site-taal (NL toont Fase, Stap, Taak via ERPNext-vertalingen).

---

## A.2 De methodiek

Elk project in Span doorloopt drie macro-fases in een vaste volgorde. Elke fase heeft een variabel aantal stappen. Tussen Doorgronden en Realiseren ligt een formeel beslismoment (poort).

### A.2.1 Overzicht van de drie fases

| # | Fase | Engelse key | Stappen | Kern |
|---|------|-------------|---------|------|
| 1 | Doorgronden | Phase | 4 | Analyse, scope, architectuur, vaste prijs |
| 2 | Realiseren | Phase | 4 | Ontwerp, bouw, migratie, testen |
| 3 | Implementeren | Phase | 2 | Training, go-live en nazorg |

### A.2.2 Stappen per fase

**Fase 1: Doorgronden**

| Stap | Omschrijving |
|------|-------------|
| Stap 1 | Analyserapport |
| Stap 2 | Scope-document |
| Stap 3 | Architectuurschets |
| Stap 4 | Prijsbepaling-vaste-prijs |

**Fase 2: Realiseren**

| Stap | Omschrijving |
|------|-------------|
| Stap 1 | Ontwerp en Architectuur |
| Stap 2 | Ontwikkeling en Configuratie |
| Stap 3 | Data-migratie |
| Stap 4 | Testen en Validatie |

**Fase 3: Implementeren**

| Stap | Omschrijving |
|------|-------------|
| Stap 1 | Training |
| Stap 2 | Go-live en Nazorg |

### A.2.3 Poorten

Een poort is een harde gate tussen twee fases. Fase N moet volledig afgerond zijn voordat aan Fase N+1 gewerkt mag worden. Er zijn twee poorten:

1. **Beslismoment** (poort na Fase 1): de klant neemt een Go/No-Go-beslissing en kiest een tier (Basis, Plus of Premium). Na akkoord en aanbetaling volgt de Kick-off van het projectteam en start Fase 2.
2. **Poort na Fase 2**: Fase 2 is afgesloten (testen en validatie gereed) voordat Fase 3 (Implementeren) begint. Deze poort heeft geen aparte naam maar werkt identiek als harde gate.

```
Doorgronden --> [Beslismoment] --> Realiseren --> [Poort] --> Implementeren
```

---

## A.3 De werkhierarchie

Span organiseert werk in een vijflaagse boom. Twee niveaus zijn groeperingen (Phase, Step/Epic); de onderste laag bevat het uitvoerbare werk (Story, Bug, Task).

### A.3.1 Niveaus

| Niveau | Engelse key | NL-weergave | Type | Omschrijving |
|--------|-------------|-------------|------|-------------|
| 1 | Project | Project | Groep | De volledige opdracht voor een klant. |
| 2 | Phase | Fase | Groep | Een van de drie methodiek-fases. Hangt altijd onder een Project. |
| 3 | Step | Stap | Groep | Een deelopdracht binnen een Fase. Hangt altijd onder een Phase. |
| 4 | Epic | Epic | Groep | Een groot feature-thema dat stories bundelt. Altijd Engels, ook in NL-omgeving. |
| 5 | Story / Bug / Task | Story / Bug / Taak | Werk | Het uitvoerbare werk-item. Story = eis als gebruikerswaarde; Bug = defect; Task = concreet werkstuk. |

### A.3.2 Twee harde structuurregels

1. **Een Phase hangt altijd onder een Project.** Een Phase zonder Project-ouder is niet geldig.
2. **Een Step hangt altijd onder een Phase.** Een Step zonder Phase-ouder is niet geldig.

Op elk ander niveau mogen losse taken worden toegevoegd zonder Epic-tussenlaag.

### A.3.3 Taalregel

De datalaag (veldkeys, doctype-namen, interne waarden) gebruikt altijd Engelse termen: `Phase`, `Step`, `Task`. De weergave in de interface volgt de ingestelde site-taal via ERPNext-vertalingen: `Fase`, `Stap`, `Taak`. **Epic en Story zijn altijd Engels**, ook in een volledig Nederlandstalige omgeving.

### A.3.4 NL-vertaalstrategie

Datalaag = Engelse keys/labels + Engelse select-waarden. NL-weergave komt mee met de app via `span/translations/nl.csv`. NL-termen volgen het methodiek-vocabulaire (Eis, Knelpunt, Fase, Stap, Werktype) en zijn afgestemd op de ERPNext-NL-Translation canon. Bewuste afwijking: Requirement = Eis (domein-woord) in plaats van canon Vereiste. Span-eigen termen worden daarnaast ook aan de canon-repo toegevoegd (in behandeling). Standaard-taaktitels: Engelse bron + NL-vertaling via `nl.csv`, zodat een NL-user ze in het Nederlands ziet.

---

## A.4 Glossarium

### Kern-concepten

| Term | Definitie |
|------|-----------|
| **Fase** (Phase) | Een van de drie methodiek-fases (Doorgronden, Realiseren, Implementeren). Structureel niveau 2 in de werk-boom. Hangt altijd onder een Project. |
| **Stap** (Step) | Een deelopdracht binnen een Fase (bijv. Analyserapport, Scope-document). Structureel niveau 3. Hangt altijd onder een Phase. |
| **Taak** (Task) | Het kleinste uitvoerbare werk-item in Span. Kan op elk niveau voorkomen als losse taak of als kind van Epic/Story. |
| **Epic** | Een groot feature-thema dat meerdere Stories bundelt. Altijd Engels. Structureel niveau 4. |
| **Story** | Een werk-item dat een eis uitdrukt als gebruikerswaarde ("Als gebruiker wil ik..."). Altijd Engels. Structureel niveau 5. |
| **Bug** | Een werk-item dat een defect of fout beschrijft. Structureel niveau 5. |
| **Requirement** (Eis) | Een los doctype dat vastlegt wat het systeem moet doen of zijn (het "wat"). Staat los van de werk-boom en heeft een eigen levenscyclus: Draft, Agreed, Built, Tested, Accepted (de eerste vier automatisch afgeleid uit de dekking, Accepted handmatig). Een eis heeft een type (Functioneel of Niet-functioneel), een MoSCoW-prioriteit, een herkomst (Requirement Source) en een toetsbaar acceptatiecriterium. |
| **Requirement Source** (Bron) | Een eigen doctype dat elke herkomst van een eis als first-class record vastlegt. Heeft een `type`: Problem, Process, System, Data, Role, Risk, Wish of Technical. Het oude `Pain Point`-doctype is hierin opgegaan: een knelpunt is nu een Requirement Source met `type = Problem`. Symmetrisch model: élke eis-herkomst is een gelijkwaardig record, geen aparte asymmetrie meer. Wordt opgehaald tijdens Fase 1 (Doorgronden) en vormt de bron van eisen. |
| **Requirement Link** | Een junction-record dat een werk-item (Story, Epic, Test, Task) koppelt aan een Requirement. Drie velden: het werk-item, het relatietype (implements / verifies / depends-on) en de Requirement. Maakt many-to-many-koppelingen mogelijk en draagt zelf betekenis. |

### Prioritering en tier

| Term | Definitie |
|------|-----------|
| **MoSCoW** | Prioriteringsmethode voor eisen. Vier niveaus: Must (dag-1-noodzaak, geen workaround), Should (belangrijk maar met workaround), Could (nice-to-have, eerste kandidaat bij krapte), Won't this time (bewust geparkeerd). |
| **Must** | MoSCoW-niveau 1. Zonder dit werkt het systeem niet. Vormt de grondslag voor tier Basis. |
| **Should** | MoSCoW-niveau 2. Belangrijk, maar er bestaat een tijdelijke omweg. Valt in tier Plus. |
| **Could** | MoSCoW-niveau 3. Wenselijk, wordt als eerste geschrapt als tijd of budget krap is. Valt in tier Premium. |
| **Won't** | MoSCoW-niveau 4. Bewust niet in deze opdracht. Geparkeerd als future project. |
| **Tier / Pakket** | Het niveau dat de klant kiest bij het Beslismoment. Bepaalt welke eisen en stories actief worden uitgevoerd. Vier waarden: Basis (alleen Must-eisen), Plus (Must + Should), Premium (Must + Should + Could), Future (geparkeerde Won't-items). |
| **Basis** | Tier 1. Omvat uitsluitend Must-eisen. |
| **Plus** | Tier 2. Omvat Must en Should-eisen. |
| **Premium** | Tier 3. Omvat Must, Should en Could-eisen. |
| **Future** | Niet een uitvoerbare tier maar een label voor Won't-items die voor een latere opdracht worden bewaard. |

### Verantwoordelijkheden

| Term | Definitie |
|------|-----------|
| **RACI** | Verantwoordelijkheidsmodel voor deliverables en taken. Vier rollen: R (Responsible), A (Accountable), C (Consulted), I (Informed). Gouden regel: precies één A per deliverable. |
| **R (Responsible)** | Voert het werk uit. Mag meerdere personen zijn. |
| **A (Accountable)** | Eindverantwoordelijk, tekent af. Altijd precies één persoon per deliverable of poort. |
| **C (Consulted)** | Wordt vooraf geraadpleegd en geeft input (twee-richtingsverkeer). |
| **I (Informed)** | Wordt achteraf geïnformeerd over het resultaat (één-richtingsverkeer). |

### Procesconcepten

| Term | Definitie |
|------|-----------|
| **Beslismoment** | De formele poort na Fase 1 (Doorgronden). De klant neemt een Go/No-Go-beslissing en kiest een tier (Basis, Plus of Premium). Na akkoord en aanbetaling volgt de Kick-off van het projectteam. |
| **Poort** | Een harde gate tussen twee fases. Fase N moet volledig afgerond zijn voordat Fase N+1 mag starten. Er zijn twee poorten: na Fase 1 (het Beslismoment) en na Fase 2. Poorten worden gevalideerd door Span-logica; overschrijding blokkeert de volgende fase. |

---

## A.5 Recente ontwerpbeslissingen

Onderstaande beslissingen zijn vastgelegd in het levende document `Span-Architectuur-en-Beslissingen.html` en sturen de bouw. Tenzij anders vermeld zijn ze **[GEPLAND]**.

- **RACI** [GEPLAND, fase-2]: licht mechanisme, maar alle 4 rollen behouden. R via native `_assign` (meerdere), A via `custom_accountable` (precies 1, de default-tekenaar per poort), C (Consulted) en I (Informed) via tags. De Klant tekent Scope, Prijs, Ontwerp, UAT en Go-live; de Consultant tekent de interne readiness en de migratie-go. Geen zware RACI-matrix-doctype, maar C en I blijven bestaan.
- **Beheer/SLA** [GEPLAND]: Impertio beheert het systeem doorlopend (recurring), los van de eenmalige vaste projectprijs. De klant beheert het systeem NIET zelf (technisch beheer is Impertio), maar gebruikt ERPNext wel zelf (data invoeren, eigen templates, reports en configuratie). Dit levert twee taken in Fase 3 Stap 2: "Beheeroverdracht uitvoeren" (project gaat over naar Impertio-beheer, klant krijgt gebruikstoegang) en "Beheerafspraak / SLA vastleggen" (SLA-niveau bespreekbaar).
- **Structuur-generator** [GEBOUWD]: whitelisted `span.api.rollout_span_structure(project)` rolt het lean skelet (`span/pm/span_skelet.json`, 86 rijen) uit als Task-tree (Phase/Step/Task, poorten met "◆ "-prefix). Idempotent (weigert als er al een Phase onder het project staat); registers (type register) worden NIET als taak aangemaakt. Trigger: knop "Structuur uitrollen" in de groep "Span" op het Project-formulier (`public/js/project.js`).
- **Beslismoment** [GEBOUWD]: het veld `Project.custom_decision` (waarden `Pending` / `Go` / `No-Go`, default `Pending`) draagt het Go/No-Go-besluit. Er is bewust GEEN aparte mijlpaaltaak gebouwd: de Doorgronden-poort uit het skelet ís het Beslismoment, gehandhaafd via `enforce_phase_gate` + `custom_decision`.
- **Poort HARD** [GEBOUWD]: een Phase mag pas op board_state `Done` als al haar onderliggende (niet-group) taken klaar zijn. De Doorgronden-fase vereist bovendien `Project.custom_decision == "Go"`. Geen per-step blokkade, alleen per fase. Afgedwongen via `enforce_phase_gate`.
- **Stap 4 Fase 1 = Prijsbepaling-vaste-prijs** [GEPLAND]: geen losse offerte. Het apart presenteren is geschrapt; de onderbouwde prijs + pakketten gaan per mail. De pakketkeuze is een klant-antwoord bij het Beslismoment, geen Impertio-taak.
- **Registers apart** [GEPLAND]: registers (Change-/meerwerk-log, Test-, Bevindingen-, Trainings-, Hypercare-register, etc.) zijn een apart doorlopend document (type register), geen open taak.
- **Billing in Span** [GEPLAND, geparkeerd]: facturatie-koppeling komt later in Span, nu bewust geparkeerd.
- **Lead-capture** [GEPLAND]: een aparte React-PWA, buiten de Span Frappe-app.
- **Taak-descriptions via AI** [GEPLAND]: de descriptions van de standaard-taken worden door AI gegenereerd uit de blauwdrukken.

---

# B. Datamodel & doctypes

> **Leeswijzer.** Deze sectie beschrijft hoe Span data modelleert: welke doctypes er zijn, welke velden ze dragen, en hoe ze samen de "sluitende keten" vormen van knelpunt naar werkend, getest systeem. Elk onderdeel is gemarkeerd:
>
> - **[GEBOUWD]** = bestaat in de code (custom fields, doctypes of `span/api.py`-logica) en draait op de instance.
> - **[GEPLAND]** = besloten ontwerp uit `Span-Architectuur-en-Beslissingen.html`, nog te bouwen.
>
> **Harde regel (geldt voor alles in deze sectie):** server-logica is app-Python via `doc_events` in `hooks.py`, met de `frappe.*`-namespace. **Geen Server Scripts** (die draaien in een RestrictedPython-sandbox die `import` blokkeert). Zie sectie over server-logica onderaan.

---

## B.1 Filosofie: type, niet niveau

Span legt geen aparte doctype-hierarchie op bovenop ERPNext. De volledige werkboom leeft in de **native ERPNext Task** (een NestedSet-tree via `parent_task`). Een Task krijgt een **werktype** mee, geen vast niveau. Daardoor mag je vrij nesten, met twee uitzonderingen die hard worden afgedwongen.

De werkhierarchie zoals bedoeld:

```
Project          de volledige opdracht voor een klant
 └─ Phase        Doorgronden / Realiseren / Implementeren (group)
     └─ Step     deelopdracht binnen een fase (group)
         └─ Epic     groot feature-gebied, bundelt stories (group)
             └─ Story | Bug | Task   het concrete werk
```

- **Story** = eis als gebruikerswaarde (het *hoe*).
- **Bug** = defect.
- **Task** = concreet werkstuk.

**Twee vaste structuurregels** (verder is nesten vrij; losse taken mogen op elk niveau hangen):

1. Een **Phase** hangt altijd onder een **Project**.
2. Een **Step** hangt altijd onder een **Phase**.

**Taal.** De datalaag gebruikt Engelse keys (`Phase`/`Step`/`Task`); de weergave volgt de site-taal (NL toont Fase/Stap/Taak via ERPNext-vertalingen). **Epic** en **Story** blijven altijd Engels.

---

## B.2 Uitbreidingen op Task (custom fields) **[GEBOUWD]**

Bron: `span/fixtures/custom_field.json` (module `PM`). Alle velden zitten in een eigen sectie ("Span") die direct na `status` op het Task-formulier wordt ingevoegd. Onderstaande velden worden via fixtures gereproduceerd bij `bench migrate`.

| Veld | Type | Opties / uitleg | Status |
|---|---|---|---|
| `custom_span_section` | Section Break | Visuele sectie "Span", `insert_after: status`. | [GEBOUWD] |
| `custom_work_type` | Select | `Phase / Step / Epic / Story / Task / Bug`. Default `Task`. "Type, geen niveau. Phase en Epic worden group-tasks." `in_list_view`, `in_standard_filter`. | [GEBOUWD] |
| `custom_board_state` | Select | `Backlog / Todo / In Progress / In Review / Done / Canceled` (6 kolommen). Default `Backlog`. Stuurt de kanban en synct eenrichtings naar de native `status`. `in_standard_filter`. | [GEBOUWD] |
| `custom_story_points` | Int | Optionele schatting. `non_negative`. | [GEBOUWD] |
| `custom_discipline` | Table MultiSelect | Options `Span Task Discipline` (child) -> `Span Discipline`. Cross-cutting tags (Frontend, Backend, UI/UX, DevOps); meerdere toegestaan. `in_standard_filter`. | [GEBOUWD] |
| `custom_phase` | Link -> Task | "Phase (auto)". `read_only`. Automatisch gevuld met de dichtstbijzijnde Phase-voorouder, voor plat filteren op "fase + alle children" zonder de tree. | [GEBOUWD] |
| `custom_epic` | Link -> Task | "Epic (auto)". `read_only`. Automatisch gevuld met de dichtstbijzijnde Epic-voorouder, voor "epic + bijbehorende stories". | [GEBOUWD] |
| `custom_span_section_end` | Section Break | Sluit de Span-sectie af. | [GEBOUWD] |

**Belangrijk over de twee Link-velden:** `custom_phase` en `custom_epic` zijn **afgeleide, read-only** velden. Ze worden niet handmatig gezet maar door de validate-hook gevuld (zie `set_span_ancestors` in B.7). Ze maken plat filteren mogelijk zonder de NestedSet te hoeven traversen.

### Uitbreidingen op Task: package en meerwerk **[GEBOUWD]**

> [GEBOUWD] (code op branch `development`; bench migrate-verificatie op de instance nog te doen).

| Veld | Type | Opties / uitleg | Status |
|---|---|---|---|
| `custom_package` | Select | `Basis / Plus / Premium / Future`. Per epic/story, afgeleid uit de MoSCoW-prioriteit van de gekoppelde Requirement. Houdt de reden vast (reversibel bij tier-upgrade). | [GEBOUWD] |
| `custom_meerwerk_status` | Select | `(leeg) / To Review / Approved / Future Project`, `read_only`. Scope-bewaking: een nieuw Epic/Story op een Go-project dat (nog) niet via een Requirement Link aan een eis hangt, krijgt automatisch `To Review` (zie `flag_meerwerk`, B.8.3). Een Projects Manager zet het op `Approved` of `Future Project`. | [GEBOUWD] |

---

## B.3 Uitbreidingen op Project (custom fields) **[GEBOUWD]**

> [GEBOUWD] (code op branch `development`; bench migrate-verificatie op de instance nog te doen). De tier-cancel-logica is meegebouwd in fase 2 (zie B.8.3).

| Veld | Type | Opties / uitleg | Status |
|---|---|---|---|
| `custom_tier` | Select | `Basis / Plus / Premium`. Gezet op het Beslismoment (Go/No-Go) na Doorgronden. Triggert de tier-cancel-logica (zie B.8.3). | [GEBOUWD] |
| `custom_decision` | Select | `Pending / Go / No-Go`, default `Pending`. Het Go/No-Go-besluit aan het Beslismoment (de poort na Doorgronden). De Doorgronden-fase mag pas op `Done` als dit veld op `Go` staat (zie `enforce_phase_gate`, B.8.3). | [GEBOUWD] |

---

## B.4 Span Discipline (master) **[GEBOUWD]**

Bron: `span/pm/doctype/span_discipline/span_discipline.json`. Master-lijst van cross-cutting disciplines (Frontend, Backend, UI/UX, DevOps) die dwars door de hele werkboom heen als tags worden gebruikt. Wordt via fixtures uitgeleverd.

| Veld | Type | Opties / uitleg | Status |
|---|---|---|---|
| `discipline_name` | Data | `reqd`, `unique`, `in_list_view`. Tevens de naam (autoname `field:discipline_name`, `naming_rule: By fieldname`). | [GEBOUWD] |
| `color` | Color | Optionele kleur voor weergave/indicatoren. | [GEBOUWD] |

Eigenschappen: `track_changes=1`, niet submittable. Permissies: System Manager (volledig), Projects Manager (create/read/write), Projects User (read).

---

## B.5 Span Task Discipline (child junction) **[GEBOUWD]**

Bron: `span/pm/doctype/span_task_discipline/span_task_discipline.json`. Dit is de child-table (`istable: 1`, `editable_grid: 1`) achter het Table MultiSelect-veld `custom_discipline` op Task. Eén rij per gekoppelde discipline.

| Veld | Type | Opties / uitleg | Status |
|---|---|---|---|
| `discipline` | Link -> Span Discipline | `reqd`, `in_list_view`. De enige kolom; het MultiSelect-patroon doet de rest. | [GEBOUWD] |

> Dit is het Frappe-patroon voor many-to-many tags: `custom_discipline` (Table MultiSelect op Task) -> `Span Task Discipline` (child rows) -> `Span Discipline` (master).

---

## B.6 Het eisen-vlak: Requirement, Requirement Link, Requirement Source **[GEBOUWD]**

> [GEBOUWD] (code op branch `development`; bench migrate-verificatie op de instance nog te doen). De doctypes `Requirement`, `Requirement Link` en `Requirement Source` bestaan in de code op `development`. De afgeleide server-logica (eis-status-roll) en het dekkingsrapport (Span Coverage) zijn in fase 2 meegebouwd, zie B.8.3. Het oude `Pain Point`-doctype is verwijderd en opgegaan in Requirement Source (`type = Problem`).

Het besloten ontwerp introduceert een **tweede vlak** naast de werkboom. Een eis is het *wat*, een story het *hoe*. Ze leven naast elkaar en klikken aan elkaar vast via een junction. Een eis is bewust **geen Task-type**, omdat:

- een Task precies één ouder heeft (dus geen many-to-many mogelijk is);
- eisen anders de project-voortgang zouden vervuilen;
- het contract (*wat*) los moet staan van de uitvoering (*hoe*); de eis heeft een eigen levenscyclus.

### B.6.1 Requirement (los doctype) **[GEBOUWD]**

> [GEBOUWD] (code op branch `development`; bench migrate-verificatie op de instance nog te doen).

De eis als contract. Lean gehouden: genoeg om contract te zijn, niet meer. `track_changes=1`, **niet** `is_submittable`. De selectwaarden zijn Engels (datalaag), de NL-weergave komt via `nl.csv` (zie A.3.4).

| Veld | Type | Opties / uitleg | Status |
|---|---|---|---|
| `requirement_id` | Data | `read_only`. Leesbare code, autoname `F-01` / `NFR-01` per project (per-project teller); docname `{project}-{id}`. | [GEBOUWD] |
| `type` | Select | `Functional / Non-Functional`. | [GEBOUWD] |
| `title` | Data | Toetsbare titel. | [GEBOUWD] |
| `priority` | Select | MoSCoW: `Must / Should / Could / Won't`. Stuurt tier/scope (zie B.6.4). | [GEBOUWD] |
| `status` | Select | `Draft / Agreed / Built / Tested / Accepted`. De eerste vier worden automatisch afgeleid uit de Requirement Link-dekking (zie B.6.3); `Accepted` is het handmatige eindbesluit en wordt door de roll nooit overschreven. | [GEBOUWD] |
| `project` | Link -> Project | `reqd`. Het project waartoe de eis behoort. | [GEBOUWD] |
| `description` | Text Editor | Toetsbare omschrijving. | [GEBOUWD] |
| `acceptance_criterion` | Small Text | De Definition of Done van de eis. | [GEBOUWD] |
| `source` | Link -> Requirement Source | De concrete bron van de eis (knelpunt, proces, systeem, regelgeving, wens). Vervangt de oude Pain Point-link; élke herkomst is nu een first-class Requirement Source. | [GEBOUWD] |
| `source_type` | Select | `read_only`, `fetch_from: source.type`. Spiegelt het type van de gekoppelde Requirement Source: `Problem / Process / System / Data / Role / Risk / Wish / Technical`. | [GEBOUWD] |
| `source_document` | Data | Verwijzing naar het brondocument. | [GEBOUWD] |

### B.6.2 Requirement Link (junction) **[GEBOUWD]**

> [GEBOUWD] (code op branch `development`; bench migrate-verificatie op de instance nog te doen).

Eén los recordje per koppeling: "dit werk-item *doet iets* met die eis". Standaard junction-doctype dat many-to-many mogelijk maakt (één eis aan veel stories en omgekeerd) en zelf betekenis draagt.

| Veld | Type | Opties / uitleg | Status |
|---|---|---|---|
| `requirement` | Link -> Requirement | Welke eis. | [GEBOUWD] |
| `work_item` | Link -> Task | Welk werk-item (epic / story / test). | [GEBOUWD] |
| `relation_type` | Select | `implements / verifies / depends-on`. | [GEBOUWD] |
| `note` | Text | Optioneel: coverage of toelichting. | [GEBOUWD] |

> Lees een rij als een zin: "Story IFC-render **implements** F-01". Twee stories kunnen samen F-01 dekken; een UAT-test **verifies** F-02. Precies daarom kan de eis geen boom-knoop zijn.

### B.6.3 Eis-status: automatisch afgeleid **[GEBOUWD]**

`derive_requirement_status(req)` leidt `Requirement.status` af uit de Requirement Link-dekking. De keten is **Draft -> Agreed -> Built -> Tested**; `Accepted` is een handmatig eindbesluit en wordt door de roll nooit overschreven.

| Status | Voorwaarde |
|---|---|
| **Draft** | Geen `implements`-link. |
| **Agreed** | Minstens 1 `implements`-link, maar niet alle implementerende stories zijn Done. |
| **Built** | Alle implementerende stories zijn Done. |
| **Tested** | Built, én alle `verifies`-tests zijn Done. |
| **Accepted** | Handmatig eindbesluit (UAT-aftekening). Niet overschreven door de roll. |

De roll wordt getriggerd via `requirement_link_changed` (Requirement Link `after_insert` / `on_update` / `on_trash`) en `roll_requirements_for_task` (Task `on_update`).

### B.6.4 MoSCoW -> tier/package **[GEPLAND]**

De prioriteit op de eis bepaalt het pakket en daarmee de scope:

| MoSCoW | Betekenis | Pakket |
|---|---|---|
| Must | zonder dit werkt het niet, dag-1-noodzaak | BASIS |
| Should | belangrijk, maar er is een workaround | +PLUS |
| Could | nice-to-have, eerst geschrapt bij krapte | +PREMIUM |
| Won't (this time) | bewust niet nu, geparkeerd | Future |

### B.6.5 Requirement Source (de bron) **[GEBOUWD]**

> [GEBOUWD] (code op branch `development`; bench migrate-verificatie op de instance nog te doen).

Generiek getypeerd bron-doctype, zodat élke eis-herkomst een first-class record is (symmetrisch model, geen asymmetrie meer). Vervangt het oude `Pain Point`-doctype: een knelpunt is nu een Requirement Source met `type = Problem`. Datalaag = Engelse keys/labels; admin-helpteksten in `nl.csv` (zie A.3.4).

| Veld | Type | Opties / uitleg | Status |
|---|---|---|---|
| `source_id` | Data | `read_only`. Leesbare code via controller-autoname, per project per type. Docname = `{project}-{source_id}`. | [GEBOUWD] |
| `type` | Select | `Problem / Process / System / Data / Role / Risk / Wish / Technical`. Bepaalt de autoname-prefix (zie hieronder). | [GEBOUWD] |
| `project` | Link -> Project | `reqd`. Het project. | [GEBOUWD] |

**Autoname-prefixes per type** (per-project teller):

| `type` | Prefix | Voorbeeld |
|---|---|---|
| Problem | `K` | `K-01` |
| Wish | `W` | `W-01` |
| Risk | `R` | `R-01` |
| Technical | `T` | `T-01` |
| Process | `P` | `P-01` |
| System | `S` | `S-01` |
| Data | `D` | `D-01` |
| Role | `RO` | `RO-01` |

---

## B.7 De sluitende keten

De kern van het datamodel is dat elke schakel mechanisch aan de volgende hangt. Klik een eis en je ziet de hele keten; een ontbrekende schakel is een scope-gat of test-gat.

Pijlen dragen de **echte Requirement-Link-namen**, in de richting die ze waarmaakt: traceerbaarheid terug naar de bron.

```
Requirement Source  ◄──source──  Requirement  ◄──implements──  Epic / Story  ──►  Task
(de bron, type)                  (de eis, wat)  ◄──verifies────  Test           (het werk)
                                     ▲ depends-on (eis -> eis)
```

**Definitieve pijl-semantiek** (Requirement Link `relation_type`):

- **Story -> Requirement**: `implements`.
- **Test -> Requirement**: `verifies`.
- **Requirement -> Requirement Source** (de bron/knelpunt): `source` (`Requirement.source`, Link -> Requirement Source; `source_type` fetch_from `source.type`).
- **Requirement -> Requirement**: `depends-on` (afhankelijkheid tussen eisen, indien nodig).

Boxes kunnen meerdere in- en uit-links hebben (**M:N**): meerdere stories onder één eis, meerdere eisen op één bron.

- **Bron <-> Requirement**: `Requirement.source` (Link -> Requirement Source) + `source_type` (fetch_from). **[GEBOUWD]**
- **Requirement <-> Epic/Story/Test**: via **Requirement Link** (many-to-many, met `relation_type`). **[GEBOUWD]**
- **Epic -> Story -> Task**: de native ERPNext Task-tree (`parent_task`), getypeerd via `custom_work_type`. **[GEBOUWD]**
- **Test verifies Requirement**: een werk-item met een Requirement Link van type `verifies`. **[GEBOUWD]**

Wat de keten oplevert (alles **[GEBOUWD]**):

- **Rode draad als live rapport**: bron -> eis -> story -> taak -> test, mechanisch. "Toon alles wat aan F-01 hangt" is één query.
- **Tier afgeleid**: MoSCoW op de eisen geeft BASIS/PLUS/PREMIUM; de tierkeuze cancelt automatisch het werk boven de tier (zie tier-cancel, B.8.3).
- **Dekking automatisch**: het **Span Coverage**-rapport toont scope-gaten (eis zonder story) en test-gaten (eis zonder verifiërende test). Geen handwerk. Zie B.8.3.
- **Change-impact**: een wijziging raakt eis X, dus welke stories en tests moeten herzien worden, in één klik.

---

## B.8 Server-logica op het datamodel

**Harde regel:** server-logica draait als app-Python via `doc_events` in `span/hooks.py`, met de `frappe.*`-namespace. **Geen Server Scripts** (RestrictedPython blokkeert `import`). De docstring van `span/api.py` zegt dit expliciet: "Imports zijn hier toegestaan, in tegenstelling tot Server Scripts."

### B.8.1 Geregistreerde events **[GEBOUWD]**

In `hooks.py`:

```python
doc_events = {
    "Task": {
        "validate": "span.api.task_validate",
        "on_update": "span.api.roll_requirements_for_task",
    },
    "Requirement Link": {
        "after_insert": "span.api.requirement_link_changed",
        "on_update": "span.api.requirement_link_changed",
        "on_trash": "span.api.requirement_link_changed",
    },
    "Project": {
        "on_update": "span.api.project_tier_changed",
    },
}
```

`task_validate` draait **na** de ERPNext-controller-validate, dus de hier gezette status overschrijft die van ERPNext (gewenst voor de bord-sync). Het is het centrale punt voor alle Span-Task-logica en roept de volgende functies aan:

| Functie in `api.py` | Wat het doet | Status |
|---|---|---|
| `enforce_group_for_work_type(doc)` | Zet `is_group=1` als `custom_work_type` in `GROUP_WORK_TYPES` (`{"Phase", "Step", "Epic"}`) zit. Zet `is_group` nooit terug naar 0 (NestedSet blokkeert ontgroepen van een task met kinderen). | [GEBOUWD] |
| `enforce_structure_rules(doc)` | Dwingt de twee structuurregels af: een Phase vereist `project` (anders `frappe.throw`); een Step vereist een Phase-voorouder via `_has_phase_ancestor`. | [GEBOUWD] |
| `set_span_ancestors(doc)` | Loopt de `parent_task`-keten omhoog en vult `custom_phase` en `custom_epic` met de dichtstbijzijnde Phase- resp. Epic-voorouder. | [GEBOUWD] |
| `sync_board_state_to_status(doc)` | Mapt `custom_board_state` -> native `status` volgens `BOARD_STATE_TO_STATUS`. Eenrichting. | [GEBOUWD] |
| `enforce_dependencies(doc)` | Harde `depends_on`-blokkade. Een taak mag pas naar board_state `Todo / In Progress / In Review / Done` als al haar native `depends_on`-taken `Done` of `Canceled` zijn. `Backlog` blijft altijd vrij. | [GEBOUWD] |
| `enforce_phase_gate(doc)` | Een Phase mag pas op board_state `Done` als al haar onderliggende (niet-group) taken klaar zijn. De Doorgronden-fase vereist bovendien `Project.custom_decision == "Go"` (het Beslismoment / Go-No-Go). | [GEBOUWD] |
| `flag_meerwerk(doc)` | Een nieuw Epic/Story op een Go-project zonder Requirement Link naar een geaccepteerde eis krijgt automatisch `custom_meerwerk_status = "To Review"`. Zichtbaar maken, niet blokkeren. | [GEBOUWD] |

**Overige event-handlers (buiten `task_validate`):**

| Functie in `api.py` | Trigger | Wat het doet | Status |
|---|---|---|---|
| `roll_requirements_for_task(doc)` | Task `on_update` | Herberekent de status van de aan deze taak gekoppelde eisen (zie B.6.3). | [GEBOUWD] |
| `requirement_link_changed(doc)` | Requirement Link `after_insert` / `on_update` / `on_trash` | Triggert `derive_requirement_status` voor de betrokken eis (zie B.6.3). | [GEBOUWD] |
| `project_tier_changed(doc)` | Project `on_update` | Zodra `Project.custom_tier` wijzigt, roept `cancel_work_above_tier` aan: annuleert alle (niet-group) taken met een hoger `custom_package` dan de tier (rang Basis<Plus<Premium<Future). Annulering via echte `doc.save()` zodat `track_changes` een **Version** vastlegt (scope-audittrail). | [GEBOUWD] |

> Let op: `GROUP_WORK_TYPES` in de code bevat `Phase`, `Step` én `Epic`. De docstrings noemen soms alleen "Phase/Epic", maar de constante en `enforce_group_for_work_type` behandelen alle drie als group-task.

### B.8.2 Board -> status sync is EENRICHTING **[GEBOUWD]**

Het kanban-bord (`custom_board_state`) stuurt de native ERPNext `status`, nooit andersom. De mapping in `BOARD_STATE_TO_STATUS` (`api.py`):

| `custom_board_state` | native `status` |
|---|---|
| Backlog | Open |
| Todo | Open |
| In Progress | Working |
| In Review | Pending Review |
| Done | Completed |
| Canceled | Cancelled |

`sync_board_state_to_status` zet de status alleen bij een gemapte board-state; anders blijft de bestaande status (inclusief `Overdue`) ongemoeid. `Overdue` en `Template` staan bewust niet in de map: `Overdue` beheert ERPNext zelf op einddatum, en er is geen bord-kolom die ernaar mapt. **Uren raken de status hier nooit.**

### B.8.3 Fase-2 server-logica en rapportage **[GEBOUWD]**

> [GEBOUWD] in fase 2 (branch `development`, commits 49e37ab -> 8d8ea65). De afdwinging staat; de meeste functies zijn hierboven in B.8.1 al als handler beschreven.

| Functie | Wat het doet | Status |
|---|---|---|
| Structuur-generator | Whitelisted `span.api.rollout_span_structure(project)` rolt het lean skelet (`span/pm/span_skelet.json`, 86 rijen) uit als Task-tree (Phase/Step/Task, poorten met "◆ "-prefix). Idempotent (weigert als er al een Phase is); registers (type register) worden NIET als taak aangemaakt. Trigger: knop "Structuur uitrollen" (groep "Span") op het Project-formulier (`public/js/project.js`). | [GEBOUWD] |
| Tier-cancel | `project_tier_changed` -> `cancel_work_above_tier`: zodra `Project.custom_tier` wijzigt, worden alle (niet-group) taken met een hoger `custom_package` dan de tier geannuleerd (rang Basis<Plus<Premium<Future). `custom_package` houdt de reden vast, dus reversibel bij tier-upgrade. Annulering via echte `doc.save()` zodat een **Version** wordt gelogd. | [GEBOUWD] |
| Eis-status-roll | `derive_requirement_status` leidt `Requirement.status` (Draft/Agreed/Built/Tested) af uit de Requirement Link-dekking; `Accepted` blijft handmatig. Getriggerd via `requirement_link_changed` en `roll_requirements_for_task`. Zie B.6.3. | [GEBOUWD] |
| Per-fase harde poorten | `enforce_phase_gate`: een Phase mag pas op `Done` als al haar onderliggende taken klaar zijn. De Doorgronden-fase vereist bovendien `Project.custom_decision == "Go"` (de poort tussen Doorgronden en Realiseren). Geen per-step blokkade. | [GEBOUWD] |
| Dependency-afdwinging | `enforce_dependencies`: een taak mag pas uit `Backlog` zodra al haar native `depends_on`-taken `Done` of `Canceled` zijn. | [GEBOUWD] |
| Meerwerk-flag | `flag_meerwerk`: een Epic/Story op een Go-project zonder eis-link krijgt `custom_meerwerk_status = "To Review"`. Een Projects Manager zet het op `Approved` of `Future Project`. | [GEBOUWD] |

**Span Coverage (Script Report, ref `Requirement`)** **[GEBOUWD]**

Het dekkingsrapport sluit de keten aan de eis-kant. Per eis: aantal `implements`-stories, hoeveel Done, aantal `verifies`-tests, hoeveel Done, en een dekkingsoordeel:

| Oordeel | Betekenis |
|---|---|
| Scope Gap | geen story (`implements`-link ontbreekt) |
| Incomplete | wel stories, niet alle Done |
| Built | alle implementerende stories Done |
| Tested | Built én alle verifiërende tests Done |
| Accepted | handmatig afgetekend |

De summary toont aantal eisen, **scope-gaten**, getest/geaccepteerd en **dekkingsgraad %**. De meerwerk-kant (story zonder eis-link) verschijnt op de Task-lijst via `custom_meerwerk_status = To Review`.

**Requirement-Link UX** **[GEBOUWD]**

- Requirement-formulier: Connections-groep **"Coverage"** toont de gekoppelde Requirement Links met ingebouwde add-knop (doctype `links`).
- Task-formulier: knop **"Span > Link Requirement"** opent een nieuwe Requirement Link, voorgevuld met `work_item` + `relation_type = implements` (één klik om een To-Review-story aan een eis te hangen).

---

## B.9 Overzicht: gebouwd vs gepland

**[GEBOUWD]**

- Custom fields op Task: `custom_work_type`, `custom_board_state`, `custom_story_points`, `custom_discipline`, `custom_phase`, `custom_epic` (+ twee section breaks).
- Doctypes: `Span Discipline` (master), `Span Task Discipline` (child junction).
- Server-logica in `span/api.py` via `Task.validate`: group-enforcement, structuurregels, ancestor-vulling, eenrichtings board->status sync.

**[GEBOUWD]** (code op branch `development`; bench migrate-verificatie op de instance nog te doen)

- Doctypes: `Requirement`, `Requirement Link`, `Requirement Source` (vervangt het verwijderde `Pain Point`).
- Custom fields: `Task.custom_package`, `Task.custom_meerwerk_status`, `Project.custom_tier`, `Project.custom_decision`.
- Server-logica (fase 2): structuur-generator (`rollout_span_structure` + Project-knop), tier-cancel (Version-gelogd), eis-status-roll, `enforce_dependencies`, `enforce_phase_gate` (+ `custom_decision` voor Doorgronden), `flag_meerwerk` (zie B.8.1 / B.8.3).
- Rapportage: **Span Coverage** dekkingsrapport (Script Report, ref Requirement).
- Requirement-Link UX: Connections "Coverage" op Requirement, Task-knop "Link Requirement".

**[GEPLAND]**

- RACI licht (besloten): per poort alleen `custom_accountable` (1 tekenaar), geen volledige matrix in-app. Zie A.5. [GEPLAND, fase-2]
- `depends_on` automatisch uitrollen vanuit het skelet (het skelet heeft nog geen dependency-metadata; de afdwinging via `enforce_dependencies` staat wel).


---

# C. Gebruik

---

## C1. Voor mensen: werken in ERPNext Desk

### C1.1 Een project uitrollen: de standaardstructuur

Elk Span-project volgt dezelfde ruggengraat: drie vaste fases, elk met een vaste set stappen. Bij het aanmaken van een project genereert Span die structuur automatisch. Jij vult daarna het project-specifieke werk in.

**De vaste hiëarchie (volledig lean skelet):**

Onderstaand het complete, canonieke skelet zoals het bij projectaanmaak wordt uitgerold. Bron van waarheid: `Span-lean-skelet.json` in de workspace-root. Tasks staan genest onder hun Stap; registers zijn gemarkeerd als `(register)` en zijn een apart doorlopend document, geen open taak; poorten zijn gemarkeerd met `[POORT]`; schrijf-/maak-deliverables met `(deliverable)`.

```
Project
└─ Fase 1 · Doorgronden                                   (Phase)
   ├─ Intake-bezoek uitvoeren                             (Taak, los onder fase)
   ├─ Lead-epics/stories QA'en                            (Taak, los onder fase)
   ├─ Stap 1 · Analyserapport                             (Step)
   │  ├─ Afdelingsinterviews houden
   │  ├─ Werkvloer-observatie uitvoeren
   │  ├─ Systeem- en licentie-inventarisatie (IT-landschap + jaarkosten)
   │  ├─ Data-export + kwaliteitsanalyse
   │  └─ Analyserapport opstellen                         (deliverable)
   ├─ Stap 2 · Scope-document                             (Step)
   │  ├─ MoSCoW-prioriteringssessie met klant
   │  ├─ Scope-document (functionele eisen) opstellen     (deliverable)
   │  ├─ Requirements + epics/stories in Span aanmaken
   │  └─ Dekking sluiten (dekkings-rapport)
   ├─ Stap 3 · Globale architectuurschets                 (Step)
   │  ├─ Globale architectuurschets opstellen             (deliverable)
   │  └─ Technische koppelbaarheidscheck + hosting-validatie
   ├─ Stap 4 · Prijsbepaling-vaste-prijs                  (Step)
   │  ├─ Interne calculatie + tariefbepaling
   │  ├─ Onderbouwde vaste prijs + pakketten opstellen    (deliverable)
   │  └─ Prijs + pakketten opsturen (mail)
   ├─ [POORT] Beslismoment (Go/No-Go + pakketkeuze)
   └─ [POORT] Kick-off (na aanbetaling)
└─ Fase 2 · Realiseren                                    (Phase)
   ├─ Stap 1 · Ontwerp & Architectuur                     (Step)
   │  ├─ Bronnen-inventarisatie (volumes tellen)
   │  ├─ Technisch Ontwerp Document (TOD) opstellen       (deliverable)
   │  ├─ Datamigratieplan opstellen                       (deliverable)
   │  ├─ Infrastructuur-/beveiligingsontwerp opstellen    (deliverable)
   │  ├─ Testplan opstellen                               (deliverable)
   │  └─ Ontwerp laten aftekenen door klant
   ├─ Stap 2 · Ontwikkeling & Configuratie                (Step)
   │  ├─ Omgevingen klaarzetten (dev/test/prod)
   │  ├─ Iteratief bouwen + configureren per module
   │  ├─ Maatwerk bouwen waar eis het vraagt
   │  ├─ Rollen/rechten/basisgegevens inrichten
   │  ├─ Integraties aansluiten (happy + foutpad)
   │  ├─ Tussentijds testen + demo/stop-momenten
   │  ├─ Readiness-check go/no-go (klant tekent)
   │  ├─ Change-/meerwerk-log                             (register)
   │  └─ As-built configuratie-overzicht                  (register)
   ├─ Stap 3 · Data-migratie                              (Step)
   │  ├─ Mapping-/transformatieregister                   (register)
   │  ├─ Cutover-draaiboek opstellen                      (deliverable)
   │  ├─ Proefmigratie (dry run) uitvoeren
   │  ├─ Valideren (tellen/checksums/steekproef)
   │  ├─ Correcties + herhalen tot binnen drempels
   │  ├─ Opschoning brondata uitvoeren
   │  ├─ Echte cutover volgens draaiboek
   │  ├─ Post-validatie & go/no-go
   │  ├─ Validatie-controlelog                            (register)
   │  └─ Migratierapport opstellen                        (deliverable)
   ├─ Stap 4 · Testen & Validatie                         (Step)
   │  ├─ Testregister (traceerbaarheid)                   (register)
   │  ├─ UAT-draaiboek/acceptatieprotocol opstellen       (deliverable)
   │  ├─ Interne tests (unit/integratie/systeem)
   │  ├─ Niet-functionele tests (performance/beveiliging)
   │  ├─ Bevindingen oplossen + hertesten
   │  ├─ Bevindingenregister                              (register)
   │  ├─ UAT voorbereiden
   │  ├─ UAT uitvoeren met klant
   │  ├─ Beoordelen tegen exitcriteria
   │  ├─ Testrapport opstellen                            (deliverable)
   │  └─ Acceptatiebesluit + aftekening (klant)
   └─ [POORT] Acceptatie-poort (acceptatie getekend)
└─ Fase 3 · Implementeren                                 (Phase)
   ├─ Stap 1 · Training                                   (Step)
   │  ├─ Trainingsplan opstellen                          (deliverable)
   │  ├─ Oefenomgeving en trainingsaccounts klaarzetten
   │  ├─ Schermafbeeldingen maken (na inrichting)
   │  ├─ Trainingsmateriaal en handleidingen maken        (deliverable)
   │  ├─ Trainingsregister                                (register)
   │  ├─ Trainingssessies geven
   │  ├─ Feedback verzamelen
   │  ├─ Follow-up voor niet-competente deelnemers
   │  └─ Trainingsverslag opstellen                       (deliverable)
   └─ Stap 2 · Go-live & Nazorg                           (Step)
      ├─ Go-live-draaiboek opstellen                      (deliverable)
      ├─ Go/no-go-vergadering
      ├─ Cutover en smoke test
      ├─ Hypercare-log                                    (register)
      ├─ Hypercare/nazorg uitvoeren
      ├─ Beheeroverdracht uitvoeren                       (naar Impertio-beheer)
      ├─ Beheerafspraak / SLA vastleggen
      ├─ Evaluatiegesprek met klant
      └─ Evaluatierapport opstellen                       (deliverable)
```

**Altijd gegenereerd vs per project.** Dit skelet (alle fases, stappen en standaard-taken hierboven) wordt bij elk project altijd uitgerold, identiek. De project-specifieke laag (Epics en Stories) wordt per project afgeleid uit de eisen die in Stap 2 (Scope-document) zijn vastgelegd, en hangt onder de juiste Stap.

#### Lean-analyse standaard-taken

De taakverdeling van het skelet is lean ontworpen, bepaald via een multi-agent analyse tegen de blauwdrukken. Het principe:

- **Handeling = eigen taak.** Elke concrete handeling is een losse taak (interview, observatie, dry run, cutover, training geven).
- **Deliverable = 1 schrijf-/maak-taak.** Een op te leveren document is precies één taak (bijv. "Analyserapport opstellen", "TOD opstellen", "Migratierapport opstellen").
- **Rapport-secties, diagrammen en iteraties = geen losse taak.** Die leven als bullets onder de deliverable-taak of als Definition of Done ("iteratief bijgewerkt tot klant-herkenbaar", "herhalen tot binnen drempels"), niet als aparte taken.
- **Registers = apart document (type register).** Doorlopende logboeken (Change-/meerwerk-log, As-built, Mapping-register, Test-, Bevindingen-, Trainings- en Hypercare-register) zijn een apart doorlopend document, geen open taak in de boom.

**Twee structuurregels die Span afdwingt:**

1. Een Fase hangt altijd direct onder een Project. Zonder geselecteerd Project weigert het systeem de opslag.
2. Een Stap hangt altijd onder een Fase. Span controleert of er een Phase-voorouder in de keten zit; zonder die voorouder blokkeert de validatie.

Taken, Epics, Stories en Bugs mogen op elk niveau worden gehangen: direct onder een Project, onder een Fase, of onder een Stap. Nesting is vrij, behalve de twee regels hierboven.

**Stappen om een project te starten:**

1. Ga naar `Project` in ERPNext Desk en klik `Nieuw`.
2. Vul de naam, klant en verwachte einddatum in.
3. Span genereert automatisch de drie Fases en hun standaard-Stappen inclusief vaste taken.
4. Open Fase 1 (Doorgronden) en voeg project-specifieke Epics, Stories en taken toe aan de juiste Stap.
5. Koppel elke Story aan een Eis via een `Requirement Link` (zie C1.4).

---

### C1.2 Het kanban-board

Het kanban-board toont alle taken van één project verdeeld over zes kolommen. Je kiest het board via de Project-pagina of via de Span-werkruimte in Desk.

**De zes kolommen en hun betekenis:**

| Kolom | Wat het betekent |
|---|---|
| Backlog | Geidentificeerd maar nog niet gepland |
| Todo | Gepland voor deze sprint of periode |
| In Progress | Actief in uitvoering |
| In Review | Klaar voor review of beoordeling |
| Done | Afgerond |
| Canceled | Niet uitgevoerd (buiten scope of geannuleerd) |

**Slepen stuurt de status. Uren nooit.**

Wanneer je een kaartje van de ene kolom naar de andere sleept, past Span automatisch de native ERPNext-status aan:

| Board-kolom | ERPNext-status |
|---|---|
| Backlog | Open |
| Todo | Open |
| In Progress | Working |
| In Review | Pending Review |
| Done | Completed |
| Canceled | Cancelled |

Het invullen van uren (timesheet, expected hours) verandert de status op geen enkele manier. Tijdsregistratie en voortgangsstatus zijn volledig gescheiden.

**Let op:** als je de native status-veld direct aanpast buiten het board om, kan dat bij de volgende board-sync overschreven worden. Gebruik voor statuswijzigingen bij voorkeur het board.

---

### C1.3 De tree-weergave en group-by

De tree-weergave toont de volledige taaknesting: Project, Fase, Stap, Epic, Story. Hier zie je in één oogopslag welke taken onder welke Fase vallen en hoe ver elk niveau gevorderd is.

**Voortgang:** de projectvoortgang wordt berekend op basis van de methode `Task Completion`, dat wil zeggen het percentage afgeronde taken. Dit werkt automatisch: je hoeft niets handmatig bij te houden.

**Group-by:** via de group-by-functie filter en sorteer je het werk op andere dimensies, bijvoorbeeld op Epic of op Discipline. Zo zie je in een oogopslag welke stories bij een bepaald Epic horen of hoeveel front-end werk er nog open staat.

---

### C1.4 Disciplines als tags

Disciplines zijn labels die je op elke taak, Story, Bug of Epic kunt zetten. Ze lopen dwars door de hele hiëarchie. De vier beschikbare disciplines zijn:

- Frontend
- Backend
- UI/UX
- DevOps

Je kunt een taak meerdere disciplines geven. Disciplines zijn geen aparte structuurlaag; ze zijn een filterdimensie bovenop de bestaande nesting. Gebruik ze om te filteren: "toon alle open Backend-stories in Fase 2".

---

### C1.5 Eisen vastleggen en koppelen

Span werkt met twee parallelle vlakken: **eisen** (wat er gebouwd moet worden) en **werk** (hoe het gebouwd wordt). Ze bestaan los van elkaar en worden verbonden via een koppeling.

**De eis (Requirement):**

Een Requirement legt vast wat er moet gebeuren, los van hoe het uitgevoerd wordt. Een eis heeft altijd:

- Een identificatiecode (zoals `F-01` of `NFR-01`)
- Een type (Functioneel of Niet-functioneel)
- Een prioriteit volgens MoSCoW (Must, Should, Could, Won't)
- Een herkomst via `source` (Link -> Requirement Source); `source_type` wordt automatisch overgenomen uit de bron
- Een acceptatiecriterium: de definitie van wanneer de eis klaar is
- Een status: `Draft`, `Agreed`, `Built`, `Tested` of `Accepted`. De eerste vier leidt Span automatisch af uit de Requirement Link-dekking; `Accepted` teken je handmatig af.

**De bron (Requirement Source):**

Elke herkomst van een eis is een eigen record met een `type` (Problem, Process, System, Data, Role, Risk, Wish, Technical). Een knelpunt uit het Analyserapport is een Requirement Source met `type = Problem` (autoname `K-01`). Koppel de eis aan de bron via het `source`-veld, zodat de keten terugloopt tot de oorzaak.

**De koppeling (Requirement Link):**

Een Requirement Link verbindt een werk-item (taak, story, test) met een eis. Elk koppelrecord heeft drie velden:

- `work_item`: de taak of story die iets met de eis doet
- `relation_type`: `implements`, `verifies` of `depends-on`
- `requirement`: de eis waarnaar verwezen wordt

Lees een koppeling als een zin: "Story X implementeert eis F-01." Een eis kan aan meerdere stories hangen en een story kan meerdere eisen implementeren.

**Wanneer koppelen:**

1. Schrijf tijdens Stap 2 (Scope-document) de eisen in de Requirement-catalogus.
2. Maak Epics en Stories aan op basis van de eisen.
3. Koppel elke Story aan de bijbehorende eis via `Requirement Link` met relatietype `implements`.
4. Koppel testresultaten aan eisen via relatietype `verifies`.
5. Gebruik het dekkingsrapport om te controleren of elke Must-eis minstens een Story heeft (scope-gaten) en of elke eis een test heeft (risico-gaten).

---

### C1.6 Pakketten en tiers

Na Fase 1 kiest de klant een pakket: Basis, Plus of Premium. Die keuze bepaalt welke Stories en Epics daadwerkelijk gebouwd worden.

**De drie niveaus:**

| Pakket | MoSCoW-eisen inbegrepen |
|---|---|
| Basis | Alle Must-eisen |
| Plus | Must en Should |
| Premium | Must, Should en Could |
| Future | Bewust buiten scope geparkeerd |

Het veld `custom_tier` op het Project registreert de gekozen tier. De velden `custom_package` op Epics en Stories registreren op welk niveau elk werkitem valt. Zodra je `custom_tier` zet, annuleert Span (`cancel_work_above_tier`) automatisch alle werk-items boven de gekozen tier (rang Basis<Plus<Premium<Future). De annulering loopt via een echte save, zodat elke flip als **Version** wordt vastgelegd (scope-audittrail). De packagewaarde blijft bewaard, zodat bij een tier-upgrade de Stories eenvoudig teruggezet kunnen worden.

---

### C1.7 Fase-poorten: wat is een gate, wie tekent af

Na elke fase zit een harde poort. Een poort betekent: Fase N moet volledig afgerond zijn voordat aan Fase N+1 gewerkt mag worden. Span valideert dit.

**De Beslispoort (tussen Fase 1 en Fase 2):**

Dit is de belangrijkste poort. Na Doorgronden beslist de klant of het project doorgaat en op welk pakketniveau. Het besluit staat in `Project.custom_decision` (`Pending` / `Go` / `No-Go`). Span dwingt de poort af via `enforce_phase_gate`: de Doorgronden-fase mag pas op board_state `Done` als (a) al haar onderliggende taken klaar zijn én (b) `custom_decision == "Go"`. Er is bewust geen aparte mijlpaaltaak; de Doorgronden-poort uit het skelet ís het Beslismoment. Bij een Go-beslissing:

1. De klant kiest Basis, Plus of Premium (`Project.custom_tier`).
2. Span annuleert het werk boven de gekozen tier (tier-cancel, zie C1.6).
3. Fase 2 (Realiseren) wordt vrijgegeven.

**Wie tekent af:**

Elke poort heeft precies een verantwoordelijke die het aftekent: de Accountable, in Span het veld `custom_accountable` op de Stap of poort (precies 1 per poort). Er is altijd maar een persoon die akkoord geeft. De Consultant is doorgaans de Responsible (voert het werk uit) via `_assign`. De Klant tekent Scope, Prijs, Ontwerp, UAT en Go-live; de Consultant tekent de interne readiness en de migratie-go. C (Consulted) en I (Informed) worden licht bijgehouden via tags. [GEPLAND, fase-2]

---

## C2. Voor AI/agents: Span correct uitlezen en vullen

### C2.1 Doctype- en veldconventies

Span werkt uitsluitend via custom fields op bestaande ERPNext-doctypes en via twee nieuwe doctypes. Alle Span-eigen velden dragen het prefix `custom_`.

**Relevante custom fields op Task:**

| Veld | Type | Waarden |
|---|---|---|
| `custom_work_type` | Select | Phase, Step, Epic, Story, Bug, Task |
| `custom_board_state` | Select | Backlog, Todo, In Progress, In Review, Done, Canceled |
| `custom_package` | Select | Basis, Plus, Premium, Future |
| `custom_meerwerk_status` | Select | (leeg), To Review, Approved, Future Project (read_only; door `flag_meerwerk` gezet) |
| `custom_phase` | Link (Task) | Automatisch gevuld: dichtstbijzijnde Phase-voorouder |
| `custom_epic` | Link (Task) | Automatisch gevuld: dichtstbijzijnde Epic-voorouder |
| `custom_discipline` | Select (multi) | Frontend, Backend, UI/UX, DevOps |

Native `depends_on` op Task wordt door `enforce_dependencies` afgedwongen: een taak mag pas uit Backlog als al haar `depends_on`-taken Done of Canceled zijn.

**Custom fields op Project:**

| Veld | Type | Waarden |
|---|---|---|
| `custom_tier` | Select | Basis, Plus, Premium |
| `custom_decision` | Select | Pending, Go, No-Go (default Pending; poort-besluit Doorgronden) |

**Nieuwe doctypes:**

- `Requirement`: de eis-catalogus (zie C1.5).
- `Requirement Link`: de koppeling tussen werk en eis (requirement, work_item, relation_type, note).
- `Requirement Source`: de herkomst van een eis (type Problem/Process/System/Data/Role/Risk/Wish/Technical). Vervangt het verwijderde `Pain Point`.

---

### C2.2 De board-status-eenrichtingsregel

ALTIJD: behandel `custom_board_state` als de primaire statusbron. De native `status` is afgeleid.

NOOIT: stel `status` direct in als je bedoelt de voortgangstatus van een taak te wijzigen. De `sync_board_state_to_status`-handler in `api.py` overschrijft de status bij elke save op basis van `custom_board_state`.

**De mapping (eenrichting, board naar status):**

```
Backlog      -> Open
Todo         -> Open
In Progress  -> Working
In Review    -> Pending Review
Done         -> Completed
Canceled     -> Cancelled
```

**Uitzonderingen die de handler bewust niet aanraakt:**

- `Overdue`: wordt door ERPNext zelf beheerd op basis van de einddatum. Geen board-kolom mapt hier naartoe.
- `Template`: gereserveerd, geen board-kolom.

Als een taak de status `Overdue` heeft en je wil de board_state wijzigen: zet `custom_board_state` op de gewenste waarde. De handler past dan de status aan naar de gemapte waarde en `Overdue` wordt overschreven.

---

### C2.3 Structuurregels en validatie

Span dwingt twee harde structuurregels af via `enforce_structure_rules` in `api.py`. Een agent die deze regels schendt, krijgt een `frappe.throw`-fout terug bij het opslaan.

**Regel 1: Phase onder Project**

ALTIJD: zet het veld `project` op een taak met `custom_work_type == "Phase"` voordat je opslaat. Een Phase zonder project veroorzaakt een validatiefout.

**Regel 2: Step onder Phase**

ALTIJD: zorg dat een taak met `custom_work_type == "Step"` een Phase-node ergens in de `parent_task`-keten heeft. De check loopt de hele keten omhoog. Een directe ouder kan ook een Step zijn, zolang ergens hoger een Phase zit.

**Overige werktypen:**

Tasks, Stories, Bugs en Epics mogen op elk niveau worden gehangen. Geen extra structuurbeperking.

**Group-types (is_group automatisch):**

De werktypen Phase, Step en Epic zijn group-tasks. Span zet `is_group = 1` automatisch bij het opslaan als het werktype overeenkomt. Een agent hoeft `is_group` niet handmatig te zetten voor deze typen. NOOIT `is_group` naar 0 terugtrekken op een node met kinderen: ERPNext blokkeert dit en gooit een fout.

---

### C2.4 Ancestor-velden: custom_phase en custom_epic

Span berekent `custom_phase` en `custom_epic` automatisch bij elke save via `set_span_ancestors`. Ze bevatten de naam (docname) van de dichtstbijzijnde Phase respectievelijk Epic-voorouder in de keten.

NOOIT: deze velden handmatig invullen of overschrijven. Ze zijn computed bij validate.

WEL: gebruik ze voor platte filters. "Geef alle Stories onder Phase X" kan met een simpele query op `custom_phase == "FASE-001"` zonder de tree te doorlopen.

---

### C2.5 RestrictedPython-regel: nooit import in Server Scripts

Span-server-logica leeft in `api.py` (app-Python, aangeroepen via `doc_events` in `hooks.py`). In dit bestand zijn reguliere Python-imports toegestaan.

NOOIT: gebruik `import`-statements in Frappe Server Scripts. Server Scripts draaien in een RestrictedPython-sandbox waar alle `import` geblokkeerd is.

ALTIJD: gebruik de `frappe.*`-namespace in alle geautomatiseerde acties die als Server Script worden uitgevoerd. Voorbeelden:
- `frappe.utils.nowdate()` in plaats van `from datetime import date; date.today()`
- `frappe.parse_json(json_string)` in plaats van `import json; json.loads(...)`
- `frappe.db.get_value(...)` voor databasetoegang
- `frappe.throw(...)` voor validatiefouten

Voor nieuwe Span-logica: voeg toe aan `api.py` en registreer de event-handler in `hooks.py` onder `doc_events`. Nooit als Server Script implementeren als de logica imports nodig heeft of complexe redenering vereist.

---

### C2.6 Eisen koppelen via Requirement Link

Wanneer een agent Stories aanmaakt op basis van een Scope-document, koppel dan elke Story aan de bijbehorende Requirement via een `Requirement Link`-record.

**Stappenplan voor een agent:**

1. Lees de Requirement-documenten voor het project op via `frappe.get_list("Requirement", filters={"project": project_name})`.
2. Maak de Story-taak aan met de juiste `custom_work_type`, `project`, en `parent_task`.
3. Maak voor elke koppeling een `Requirement Link`-record aan:
   ```python
   doc = frappe.get_doc({
       "doctype": "Requirement Link",
       "work_item": story_name,
       "requirement": requirement_name,
       "relation_type": "implements"
   })
   doc.insert()
   ```
4. Gebruik `"verifies"` voor testresultaten, `"depends-on"` voor afhankelijkheden.

**Dekkingsregel:** elke Must-eis (priority = "Must") zonder minstens een `implements`-link is een scope-gat. Controleer na het aanmaken van Stories altijd of alle Must-eisen gedekt zijn.

---

### C2.7 Tier- en packagelogica respecteren

ALTIJD: stel `custom_package` in op elke Epic en Story op basis van de MoSCoW-prioriteit van de bijbehorende Requirement:

| Requirement.priority | custom_package |
|---|---|
| Must | Basis |
| Should | Plus |
| Could | Premium |
| Won't | Future |

NOOIT: Stories of Epics aanmaken zonder `custom_package` in te stellen als er een Requirement-koppeling is.

**Bij tier-activatie (Beslispoort):**

Wanneer `Project.custom_tier` wordt ingesteld, zet Span automatisch alle Stories en Epics boven de gekozen tier naar `custom_board_state = "Canceled"`. Een agent die dit triggert via het zetten van `custom_tier`, hoeft de individuele items niet zelf te cancelen: de server-logica handelt dit af.

NOOIT: `custom_package` na de tier-keuze op bestaande records overschrijven. Het veld registreert de scope-reden en is reversibel bij een tier-upgrade. De board_state is het operationele signaal; custom_package is de scopeverantwoording.

---

### C2.8 Samenvatting: ALWAYS/NEVER-richtlijnen voor agents

**ALWAYS:**
- Stel `custom_board_state` in om de status te sturen, niet het `status`-veld direct.
- Geef een Phase altijd een `project`-veld.
- Geef een Step altijd een Phase-voorouder in de `parent_task`-keten.
- Gebruik `frappe.*`-namespace voor alle Python-logica in Server Scripts.
- Koppel Stories aan Requirements via `Requirement Link` met `relation_type = "implements"`.
- Stel `custom_package` in op basis van de MoSCoW-prioriteit van de gekoppelde eis.
- Gebruik `custom_phase` en `custom_epic` voor platte queries; vertrouw erop dat ze automatisch worden bijgewerkt.

**NEVER:**
- Stel `status` direct in als je bedoelt het kanban-position te wijzigen.
- Gebruik `import`-statements in Server Scripts.
- Maak een Phase zonder `project`-veld.
- Maak een Step zonder Phase-voorouder.
- Overschrijf `custom_phase` of `custom_epic` handmatig.
- Zet `is_group = 0` op een node met kinderen.
- Voeg logica toe als Server Script als die logica imports nodig heeft; gebruik dan `api.py` + `doc_events`.
- Overschrijf `custom_package` na de tier-keuze om individuele items te annuleren; de server-handler doet dat bij het zetten van `custom_tier`.


---

## Roadmap / bouwlijst (samenvatting)

**Doctypes [GEBOUWD]:** Requirement, Requirement Link, Requirement Source (vervangt Pain Point).
**Uitbreiden bestaand [GEBOUWD]:** Task.custom_package, Task.custom_meerwerk_status, Project.custom_tier, Project.custom_decision.
**Server-logica (app-Python via hooks) [GEBOUWD]:** structuur-generator (`rollout_span_structure` + Project-knop), tier-cancel (Version-gelogd), eis-status-roll, `enforce_dependencies`, `enforce_phase_gate` (+ custom_decision), `flag_meerwerk`.
**Rapportage [GEBOUWD]:** Span Coverage dekkingsrapport.
**Nog open (klein):** `depends_on` automatisch uitrollen vanuit het skelet (dependency-metadata ontbreekt nog; de afdwinging staat).

## Onderhoud van dit handboek

Dit handboek loopt mee met de ontwerpbeslissingen. Werk het bij zodra een beslissing wijzigt of een feature gebouwd wordt, bij voorkeur via een agent-team dat als achtergrondproces draait en de context van de huidige sessie kent. Zie de workspace `CLAUDE.md` voor de bijwerk-regel.
