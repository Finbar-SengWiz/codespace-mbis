# Plan: StudentLens Dashboard

> Source: PRD.md + SPECS.md

## Architectural Decisions

Durable decisions that apply across all phases:

- **App entry point**: `app.py` uses `st.navigation()` to define all four pages and render a persistent custom sidebar.
- **Pages**: `pages/overview.py`, `pages/budget.py`, `pages/study.py`, `pages/loan.py` — each page is thin, calling shared modules for data and calculations.
- **Database**: SQLite at `./data/studentlens.db`, created on first run. All cross-page data flows through SQLite reads, not `st.session_state`.
- **Schema — 5 tables**:
  - `income_entries`: id, source_type, amount, date (ISO-8601), work_hours (nullable)
  - `expense_entries`: id, category_name, amount, date (ISO-8601)
  - `expense_categories`: id, name, category_type (fixed/variable), budget_limit (nullable)
  - `study_tasks`: id, course, task_name, task_type, due_date, estimated_hours, logged_hours, status, priority
  - `app_settings`: key (PRIMARY KEY), value — stores overall budget limit, loan balance, graduation date
- **Deep modules**: `db.py` (all SQLite CRUD and schema init) and `calculations.py` (all computed values) have no Streamlit dependency and are independently testable.
- **No authentication**: single-user prototype only.
- **Naming**: the composite health indicator is called **Wellbeing Balance Score — Academic & Financial** throughout.

---

## Phase 1: App Shell + Database Foundation

**User stories**: 5

### What to build

A runnable Streamlit app with a persistent sidebar showing four named navigation links (Overview, Budget, Study Load, Loan Projection). Each page displays a placeholder heading. On first run, the database file and all five tables are created, and the eight default expense categories (Rent, Tuition, Transport as fixed; Food, Social, Entertainment, Power as variable) are inserted if they do not already exist. The app starts and navigates between all pages without errors.

### Acceptance criteria

- [ ] `streamlit run app.py` starts without errors
- [ ] All four pages are reachable via the sidebar
- [ ] The `./data/studentlens.db` file is created on first run
- [ ] All five tables exist in the database after startup
- [ ] The eight default expense categories are present in `expense_categories` after first run
- [ ] Re-running the app does not duplicate the default categories

---

## Phase 2: Budget — Core Data Entry

**User stories**: 8, 9, 10, 17, 18, 19

### What to build

The Budget page gains two data entry forms: one for income and one for expenses. The income form captures source type (Part-time Work, Allowance, Scholarship, Student Loan Living Costs), amount, and date; when Part-time Work is selected, a work hours field appears. The expense form captures category (from the default list), amount, and date. After submission, both forms display their recorded entries in a table below. A weekly/monthly toggle at the top of the page filters all displayed figures to the selected period — both views read from the same underlying entries with no re-entry required. Student Loan Living Costs entries are visually flagged as debt (e.g. a red "DEBT — not income" badge) in the income table.

### Acceptance criteria

- [ ] Income entry form submits and persists an income record to `income_entries`
- [ ] Work hours field appears only when source type is Part-time Work
- [ ] Expense entry form submits and persists a record to `expense_entries`
- [ ] Recorded income entries are displayed in a table on the page
- [ ] Recorded expense entries are displayed in a table on the page
- [ ] Weekly toggle shows only entries within the current calendar week
- [ ] Monthly toggle shows only entries within the current calendar month
- [ ] Student Loan Living Costs entries show a visible debt flag in the income table
- [ ] Switching the toggle does not require re-entering data

---

## Phase 3: Study Load Logger

**User stories**: 20, 21, 22, 23, 24, 25

### What to build

A new Study Load page with a task entry form capturing: course name, task name, task type (Assignment, Exam, Reading, Lab, Other), due date (optional), estimated hours, logged hours, status (To Do / In Progress / Completed / Overdue), and priority (High / Medium / Low / None). Below the form, all tasks are displayed in a table. Each task has controls to update its status and log additional hours without re-entering the full form. A clearly labelled Upcoming Deadlines panel shows all tasks with a due date within the next 7 days, sorted ascending by due date. Total logged study hours are aggregated by week and stored in a way that the Overview page can retrieve them.

### Acceptance criteria

- [ ] Task entry form submits and persists a record to `study_tasks`
- [ ] All tasks are displayed in a table after entry
- [ ] Task status can be updated from the task table without re-opening the entry form
- [ ] Logged hours can be added to an existing task
- [ ] Upcoming Deadlines panel shows only tasks due within the next 7 days
- [ ] Upcoming Deadlines panel is sorted by due date ascending
- [ ] Tasks with no due date do not appear in the Upcoming Deadlines panel
- [ ] Weekly logged hours aggregation is retrievable (used by Overview in Phase 5)

---

## Phase 4: Loan Projection Calculator

**User stories**: 26, 27, 28, 29, 30, 31, 32

### What to build

The Loan Projection page has two persistent inputs — current loan balance and expected graduation date — saved to `app_settings` so they survive page navigation and app restarts. The average weekly Student Loan Living Costs is read automatically from `income_entries`; if no entries exist, a fallback of $280/week is used and a note is shown. The projected graduation balance is displayed as a large, prominent figure using the formula: `current_balance + (weekly_living_costs × remaining_weeks)`. A line chart shows the loan trajectory from today to the graduation date. A "What if?" slider ($0–$320, $10 steps) lets the user reduce the projected weekly living costs and see the graduation figure and chart update in real time. A permanently visible `st.info` callout states that NZ student loans carry no interest while the borrower remains in New Zealand.

### Acceptance criteria

- [ ] Current balance and graduation date inputs persist across page navigation and app restarts
- [ ] Projected graduation balance is calculated and displayed prominently
- [ ] Projection reads living cost average from `income_entries` automatically
- [ ] Fallback of $280/week is used (with a visible note) when no living cost entries exist
- [ ] Trajectory line chart renders from today to the graduation date
- [ ] Moving the What-if slider updates the graduation figure and chart without a full page reload
- [ ] Slider range is $0–$320 with $10 steps
- [ ] NZ interest-free note is always visible and not hidden behind a toggle or tooltip

---

## Phase 5: Overview Homepage

**User stories**: 1, 2, 3, 4

### What to build

The Overview page assembles data from the Budget and Study modules to produce three components. First, a **Wellbeing Balance Score — Academic & Financial** tile displays a green, amber, or red colour-coded score using the formula: `(budget_util × 0.4) + ((work_hours / 15) × 0.3) + ((1 − study_hours / 20) × 0.3)`, where green < 0.5, amber 0.5–0.75, red > 0.75. Second, three week-on-week comparison cards show current week values and signed deltas (e.g. +$42, −3 hrs) for total spending, work hours, and study hours. Third, a combined chart plots work hours, study hours, and total variable spending on the same weekly time axis across recent weeks. All three components update automatically as new data is entered in other modules.

### Acceptance criteria

- [ ] Wellbeing Balance Score tile is present and colour-coded green/amber/red
- [ ] Score label reads "Wellbeing Balance Score — Academic & Financial"
- [ ] Score updates to reflect current week's budget utilisation, work hours, and study hours
- [ ] Three week-on-week comparison cards are present for spending, work hours, and study hours
- [ ] Each card shows the current week value and the signed delta from the previous week
- [ ] Combined chart displays work hours, study hours, and variable spending on the same time axis
- [ ] Combined chart covers at least the current and previous weeks
- [ ] All components show a sensible empty state when no data has been entered

---

## Phase 6: Sample Data + Tests

**User stories**: 6, 7

### What to build

Two buttons on the Overview page — **Load Sample Data** and **Clear Sample Data** — that write to and delete from all tables respectively. Sample data reflects a realistic Canterbury NZ student: part-time café or retail work at ~$23.15/hr for 15 hrs/week, Student Loan Living Costs ~$280/week, Rent ~$235/week, Food ~$80, Social ~$40, Transport ~$30, Power ~$20, with 6–8 weeks of history and 4–5 study tasks across 3 courses. Load completes and the page refreshes within 2 seconds. Clear removes all rows from all tables and returns the dashboard to an empty state.

The five test suites from SPECS.md are implemented using an in-memory SQLite database so tests are fast and leave no files on disk:
1. `db.py` CRUD round-trips (income, expense, study task, status update)
2. Wellbeing Balance Score — three colour band assertions
3. Loan projection formula and trajectory list shape
4. Sample data load/clear — minimum record count assertions per table
5. Cross-module consistency — living cost entries in `income_entries` match the value returned by the loan projection's average living cost query

### Acceptance criteria

- [ ] "Load Sample Data" populates all tables and the Overview page reflects the data within 2 seconds
- [ ] Sample data includes at least 6 weeks of income and expense entries, NZ-realistic figures
- [ ] Sample data includes at least 4 study tasks across at least 3 courses
- [ ] "Clear Sample Data" empties all tables and the dashboard returns to empty state
- [ ] All CRUD round-trip tests pass
- [ ] Balance Score tests confirm green, amber, and red thresholds
- [ ] Loan projection test confirms formula with known inputs
- [ ] Trajectory test confirms first point equals current balance
- [ ] Sample data count assertions pass after `load_sample_data()`
- [ ] Cross-module consistency test: average living cost from projection query matches Budget entries
