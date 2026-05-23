# StudentLens — Technical Specifications

## Problem Statement

Tertiary students in New Zealand simultaneously manage part-time work, student loans, living expenses, and a heavy academic schedule, yet no single tool shows how these pressures relate to each other. Students cannot easily see whether heavy work hours are eroding study time, or whether high-stress academic weeks are driving up discretionary spending. Without this visibility, students make time and money decisions without a clear picture of the consequences.

## Solution

StudentLens is a single-user, locally-run Streamlit dashboard with four pages: an Overview homepage and three dedicated modules (Budget & Expense Tracker, Weekly Study Load Logger, Student Loan Projection Calculator). All data is stored in a local SQLite database. A "Load Sample Data" button populates the entire dashboard with realistic NZ student figures so the tool can be demonstrated immediately without manual entry.

---

## User Stories

**Overview & Navigation**
1. As a student, I want to see a summary of my key financial and academic metrics on a single homepage, so that I can assess my situation at a glance.
2. As a student, I want a colour-coded Wellbeing Balance Score — Academic & Financial (green / amber / red) derived from budget utilisation, work hours, and study hours, so that I can immediately understand whether I am in a healthy or stressed position.
3. As a student, I want to see week-on-week comparison cards for total spending, work hours, and study hours showing the signed delta from the previous week, so that I can see whether my situation is improving or deteriorating.
4. As a student, I want to see a combined chart comparing my weekly work hours, study hours, and variable spending on the same time axis, so that I can spot correlations between how I spend my time and money.
5. As a student, I want to navigate between Overview, Budget, Study Load, and Loan Projection pages via a persistent sidebar, so that I can move between modules instantly.
6. As a student, I want to load a full set of realistic NZ sample data with one click, so that I can demonstrate the dashboard without manual data entry.
7. As a student, I want to clear all sample data with one click, so that I can start fresh with my own data.

**Budget & Expense Tracker**
8. As a student, I want to record income entries with a source type (Part-time Work, Allowance, Scholarship, Student Loan Living Costs), so that I can track where my money is coming from.
9. As a student, I want to record work hours alongside Part-time Work income entries, so that my paid work time appears in the cross-module overview chart.
10. As a student, I want to record expense entries against a named category with an amount and date, so that I can track where my money is going.
11. As a student, I want a default set of fixed expense categories (Rent, Tuition, Transport) and variable expense categories (Food, Social, Entertainment, Power) pre-loaded on first run, so that I do not need to configure the system from scratch.
12. As a student, I want to toggle any expense category between "fixed" and "variable", so that I can reflect my actual spending patterns.
13. As a student, I want to add custom expense categories, so that I can track spending that does not fit the defaults.
14. As a student, I want to set a spending limit for each category, so that I can manage my budget at a granular level.
15. As a student, I want to set an overall spending limit, so that I can manage my total budget without configuring every category.
16. As a student, I want to see a visual progress bar per category showing utilisation, changing colour from green to amber at 75% and red at 100%, so that I can spot overspending before it becomes a problem.
17. As a student, I want to toggle between a weekly and monthly view of my income and expenses, so that I can understand my finances at different timeframes.
18. As a student, I want both views to be derived from the same underlying entries so that I do not have to enter data twice.
19. As a student, I want Student Loan Living Costs income entries to be visually flagged as debt throughout the Budget module, so that I am aware these funds increase my loan balance rather than my net worth.

**Weekly Study Load Logger**
20. As a student, I want to add study tasks with a course name, task name, task type, due date, estimated hours, and status, so that I can track all academic commitments in one place.
21. As a student, I want to log actual hours spent on each task, so that I can compare estimated versus actual time and understand my real study load.
22. As a student, I want a dedicated Upcoming Deadlines view showing all tasks due within the next 7 days sorted by due date, so that I can plan my week without scrolling through every task.
23. As a student, I want to update the status of a task (To Do, In Progress, Completed, Overdue), so that I can track progress and identify tasks that have fallen behind.
24. As a student, I want to assign a priority level (High, Medium, Low) to each task, so that I can focus effort on what matters most.
25. As a student, I want to see total logged study hours aggregated by week, so that I can understand my study load over time and compare it with work hours and spending on the Overview page.

**Student Loan Projection Calculator**
26. As a student, I want to enter my current student loan balance, so that the projection starts from my real financial position.
27. As a student, I want to enter my expected graduation date, so that the calculator can determine how long I have left to accumulate living cost borrowing.
28. As a student, I want the calculator to automatically use my recorded Student Loan Living Costs from the Budget module to project future borrowing, so that the projection reflects my actual behaviour.
29. As a student, I want to see my estimated loan balance at graduation displayed as a clear, prominent figure, so that I can understand the long-term cost of my current lifestyle.
30. As a student, I want to see a line chart showing my loan trajectory from today to my graduation date, so that I can visualise debt growth rather than just seeing a single number.
31. As a student, I want a "What if?" slider that reduces my projected weekly living costs between $0 and $320, so that I can see in real time how spending less would lower my graduation balance.
32. As a student, I want a clear, permanently visible note explaining that NZ student loans carry no interest while I remain in New Zealand, so that I understand the rules underpinning the projection.

---

## Implementation Decisions

### Application Structure

- **Entry point**: `app.py` uses `st.navigation()` to define all four pages and render a persistent, custom sidebar. This is Streamlit's multi-page pattern that allows full control over navigation labels and icons.
- **Pages**: Four page files under `pages/` — `overview.py`, `budget.py`, `study.py`, `loan.py`. Each page is thin: it calls `db.py` for data and `calculations.py` for computed values, then renders with Streamlit widgets.
- **No shared session state between pages beyond the database**: all cross-page data flows through SQLite reads, not `st.session_state`. This keeps the data model simple and consistent.

### Database Module (`db.py`)

- **Engine**: SQLite via Python's built-in `sqlite3`. No ORM. File path: `./data/studentlens.db` (created on first run).
- **Schema initialisation**: `init_db()` creates all tables on startup if they do not exist. Safe to call on every app start.
- **Tables and key fields**:
  - `income_entries`: id, source_type (TEXT), amount (REAL), date (TEXT ISO-8601), work_hours (REAL, nullable — only populated for Part-time Work)
  - `expense_entries`: id, category_name (TEXT), amount (REAL), date (TEXT ISO-8601)
  - `expense_categories`: id, name (TEXT UNIQUE), category_type (TEXT: "fixed"/"variable"), budget_limit (REAL, nullable)
  - `study_tasks`: id, course (TEXT), task_name (TEXT), task_type (TEXT), due_date (TEXT ISO-8601, nullable), estimated_hours (REAL), logged_hours (REAL default 0), status (TEXT: "To Do"/"In Progress"/"Completed"/"Overdue"), priority (TEXT: "High"/"Medium"/"Low"/"None")
  - `app_settings`: key (TEXT PRIMARY KEY), value (TEXT) — stores overall_budget_limit and loan settings (current_balance, graduation_date) as key-value pairs
- **Sample data**: `load_sample_data()` inserts NZ-realistic records across all tables. `clear_sample_data()` deletes all rows from all tables (does not drop or recreate tables).
- **Data access functions**: simple functions that execute SQL and return lists of dicts or scalar values — e.g., `get_income_entries()`, `add_expense()`, `get_weekly_study_hours()`. No abstraction beyond what pages need.

### Calculations Module (`calculations.py`)

- **Wellbeing Balance Score — Academic & Financial**: Takes three inputs — current week's budget utilisation percentage, current week's work hours, current week's logged study hours. Formula:
  ```
  score = (budget_util × 0.4) + ((work_hours / 15) × 0.3) + ((1 - min(study_hours, 20) / 20) × 0.3)
  ```
  All inputs are clamped to [0, 1] before applying weights. Green: score < 0.5. Amber: 0.5–0.75. Red: > 0.75.
- **Loan projection**: `project_loan_balance(current_balance, graduation_date, weekly_living_costs)` returns a projected balance as a float. Formula: `current_balance + (weekly_living_costs × remaining_weeks)`. Remaining weeks calculated from today's date to graduation date.
- **Loan trajectory**: `loan_trajectory(current_balance, graduation_date, weekly_living_costs)` returns a list of `(date, balance)` tuples — one point per week from today to graduation. Used to render the line chart.
- **Week-on-week delta**: `week_delta(current_value, previous_value)` returns the signed difference. Used for the three comparison cards.
- **Weekly aggregation**: `aggregate_by_week(entries)` groups a list of dated entries by ISO week number and sums amounts or hours. Used by both Budget and Study modules for the overview chart.

### Budget Page (`pages/budget.py`)

- Income entry form: source type selector, amount, date, work hours field (shown only when source type is Part-time Work).
- Expense entry form: category selector (from `expense_categories` table), amount, date.
- Category management (secondary section): toggle fixed/variable, set per-category budget limit, add custom category. MVP can render this as an expandable section below the main forms.
- Weekly/monthly toggle: a radio button or toggle at the top of the page. Filters date range for all displayed figures and charts. Both modes read from the same `income_entries` and `expense_entries` tables.
- Budget utilisation bars: rendered per category with a limit set. Colour thresholds: green < 75%, amber 75–99%, red ≥ 100%.
- Student Loan Living Costs flag: income entries of this type display a distinct "DEBT — not income" badge or label in red/orange.

### Study Load Page (`pages/study.py`)

- Task entry form: course, task name, task type (Assignment, Exam, Reading, Lab, Other), due date (optional), estimated hours, status, priority.
- Task table: displays all tasks with an inline "log hours" and "update status" interaction. For MVP this can be a simple form per row or a selectbox-based update rather than a fully inline editable grid.
- Upcoming deadlines panel: filters tasks where due_date is within the next 7 days. Sorted ascending by due_date.

### Loan Projection Page (`pages/loan.py`)

- Inputs rendered as a sidebar form or top-of-page section: current balance (number input), graduation date (date picker).
- These inputs are persisted to `app_settings` so they survive page navigation.
- Average weekly living costs are read automatically from `income_entries` where source_type = "Student Loan Living Costs". If no entries exist, a fallback of $280/week (NZ-realistic default) is used with a note shown to the user.
- "What if?" slider: range $0–$320, step $10, default is the calculated average. Updates the graduation figure and trajectory chart in real time (Streamlit reruns on slider change).
- NZ interest-free note: displayed as a visible `st.info()` or `st.warning()` callout — always visible, not collapsible.

### Overview Page (`pages/overview.py`)

- Load Sample Data and Clear Sample Data buttons at the top of this page.
- Wellbeing Balance Score — Academic & Financial: reads current week's budget utilisation, work hours, and study hours from the database; calls `calculations.balance_score()`; renders as a large coloured metric tile with the full name as its label.
- Week-on-week cards: three `st.metric()` calls for spending, work hours, study hours, each with a delta.
- Combined chart: a Streamlit `st.line_chart()` or `st.bar_chart()` with work hours, study hours, and total variable spending on the same weekly time axis. Data sourced from `db.get_weekly_work_hours()`, `db.get_weekly_study_hours()`, and `db.get_weekly_variable_spending()`.

### Sample Data (NZ-Realistic Figures)

- Income: Part-time Work at ~$23.15/hr for 15 hrs/week; Student Loan Living Costs ~$280/week; occasional Allowance entries.
- Expenses: Rent ~$235/week (fixed), Food ~$80/week (variable), Social ~$40/week (variable), Transport ~$30/week (variable), Power ~$20/week (fixed).
- Study tasks: 4–5 tasks across 3 courses with a mix of statuses, some due within 7 days.
- Loan settings: balance ~$18,000, graduation date ~18 months from a fixed reference date.
- Data should cover 6–8 weeks of history so the overview chart shows visible trends.

---

## Testing Decisions

**What makes a good test here**: test external behaviour (what data goes in, what comes out), not implementation details (SQL string contents, widget rendering). Tests call public functions from `db.py` and `calculations.py` directly — no Streamlit rendering involved.

**Modules to test:**

1. **`db.py` — Database layer**
   - `add_income_entry()` and `get_income_entries()` round-trip: insert a record, read it back, assert the values match.
   - `add_expense()` and `get_expense_entries()` round-trip: same pattern.
   - `add_study_task()` and `get_study_tasks()` round-trip.
   - `update_task_status()`: insert a task, update its status, assert the new status is returned.

2. **`calculations.py` — Wellbeing Balance Score**
   - Score below 0.5 produces "green" with low utilisation, low work hours, high study hours.
   - Score between 0.5–0.75 produces "amber".
   - Score above 0.75 produces "red" with high utilisation, high work hours, low study hours.

3. **`calculations.py` — Loan projection**
   - `project_loan_balance(18000, graduation_date, 280)` with a known remaining_weeks produces the expected result.
   - `loan_trajectory()` returns a list whose first balance equals current_balance and whose last balance equals the projected graduation balance.

4. **`db.py` — Sample data loader**
   - After `load_sample_data()`, assert that each table contains at least the expected minimum number of records (e.g., income_entries ≥ 6, expense_entries ≥ 20, study_tasks ≥ 4).
   - After `clear_sample_data()`, assert that all tables are empty.

5. **Cross-module data consistency**
   - After `load_sample_data()`, assert that the loan projection page's living cost average (`db.get_avg_weekly_living_costs()`) matches the living cost entries in `income_entries`. This verifies that data inserted into Budget is correctly consumed by the Loan module.

All tests use an in-memory SQLite database (`":memory:"`) via a test-specific `init_db()` call so they are fast, isolated, and leave no files on disk.

---

## Out of Scope

- User accounts or authentication
- Automatic bank or credit card data synchronisation
- Data export or import (CSV, PDF, or similar)
- Push notifications or budget alerts
- Multi-currency support
- LMS or external academic system integration
- Automated loan repayment strategy simulations
- AI-driven or machine-learning insights
- Grade tracking
- Mobile optimisation
- Per-category budget limits (deferred to post-MVP; overall limit is sufficient for the demo)
- Advanced Wellbeing Balance Score configuration or user-adjustable thresholds
- Production security hardening, scalability, or uptime requirements

---

## Further Notes

- This is a prototype. Every decision should favour clarity and demonstrability over robustness or future extensibility.
- The SQLite database file is at `./data/studentlens.db` relative to the project root. The `data/` directory is created by `init_db()` on first run.
- NZ student loan assumes zero interest while the student remains in New Zealand. The Loan Projection page must state this prominently and the formula must not apply any interest rate.
- The "What if?" slider maximum is fixed at $320/week regardless of the actual average living costs in the database, representing the upper bound of realistic NZ student loan living cost disbursements.
- Sample data should cover at least 6 weeks of history so that the overview chart displays meaningful trends rather than a single data point.
- All dates stored in SQLite use ISO-8601 format (YYYY-MM-DD) for consistent sorting and filtering without date parsing libraries.
