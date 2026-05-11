# StudentLens — Product Requirements Document

## 1. Context & Purpose

### Purpose & Problem Statement

StudentLens is a personal dashboard that helps tertiary students see how their day-to-day financial decisions and academic workload interact with each other.

Tertiary students frequently manage part-time work, student loans, living expenses, and a demanding course schedule simultaneously — yet no single tool shows how these pressures relate. Students may not realise that heavy work hours are correlating with reduced study time, or that high-stress academic periods are driving up discretionary spending. This lack of visibility makes it harder to make informed decisions about time and money. StudentLens brings these data streams together in one dashboard, making the interaction between spending habits, work hours, and study load visible at a glance.

### Target Users

**Persona: The Stretched Student**
- A full-time tertiary student in New Zealand, typically aged 18–24
- Balancing part-time paid work alongside coursework
- Partly or wholly funded by a student loan (fees and/or living costs)
- Has a general sense that money and academic pressure are connected, but no clear picture of how
- Not a financial expert — needs clarity, not complexity
- Time-poor: wants quick insight, not a complex setup

### Goals & Success Metrics

| Goal | Metric | Target |
|------|--------|--------|
| Demonstrate financial-academic interaction | Combined chart of work hours, study hours, and variable spending visible on homepage | Present in prototype |
| Surface loan awareness | Loan projection module displays estimated graduation balance derived from actual living cost entries | Present in prototype |
| Enable budget discipline | User can set and visualise budget limits per category and overall | Present in prototype |
| Immediate demonstrability | Dashboard fully populated from "Load Sample Data" without manual entry | Within 2 seconds of button click |
| Data literacy | Student loan living costs are clearly distinguished from true income throughout the dashboard | Present in prototype |

---

## 2. Features & Scope

### User Stories

**Overview & Navigation**
1. As a student, I want to see a summary of my key financial and academic metrics on a single homepage, so that I can assess my situation at a glance without navigating between modules.
2. As a student, I want a "Balance Score" — a colour-coded composite indicator (green / amber / red) derived from budget utilisation, work hours, and study hours — so that I can immediately understand whether I am in a healthy or stressed position.
3. As a student, I want to see week-on-week comparison cards for total spending, work hours, and study hours, so that I can see whether my situation is improving or deteriorating without reading charts in detail.
4. As a student, I want to see a combined chart comparing my weekly work hours, study hours, and variable spending, so that I can visually spot correlations between how I spend my time and money.
5. As a student, I want to navigate between the Overview, Budget, Study Load, and Loan Projection pages via a persistent sidebar or navigation menu, so that I can move between modules instantly.
6. As a student, I want to load a full set of realistic sample data with one click, so that I can demonstrate the dashboard's capabilities immediately without manual data entry.
7. As a student, I want to clear all sample data with one click, so that I can start fresh with my own real data.

**Budget & Expense Tracker**
8. As a student, I want to record income entries with a source type (Part-time Work, Allowance, Scholarship, Student Loan Living Costs), so that I can track where my money is coming from.
9. As a student, I want to record work hours alongside each Part-time Work income entry, so that I can later see how my paid work time correlates with study time and spending.
10. As a student, I want to record expense entries against a named category with an amount and date, so that I can track where my money is going over time.
11. As a student, I want a default set of fixed expense categories (Rent, Tuition, Transport) and variable expense categories (Food, Social, Entertainment, Power), so that I do not have to configure the system from scratch.
12. As a student, I want to toggle any expense category between "fixed" and "variable", so that I can reflect my actual spending patterns.
13. As a student, I want to add custom expense categories, so that I can track spending that does not fit the defaults.
14. As a student, I want to set a spending limit for each category, so that I can manage my budget at a granular level.
15. As a student, I want to set an overall spending limit (weekly or monthly), so that I can manage my total budget without configuring every category individually.
16. As a student, I want to see how much of each category's budget limit I have used — displayed as a visual progress indicator that changes colour as utilisation increases — so that I can identify where I am overspending before it becomes a problem.
17. As a student, I want to toggle between a weekly and monthly view of my income and expenses, so that I can understand my finances at both short-term and longer-term timeframes.
18. As a student, I want both the weekly and monthly views to be derived from the same underlying entries, so that I do not have to enter data twice.
19. As a student, I want "Student Loan Living Costs" income entries to be visually flagged as debt — not true income — throughout the Budget module, so that I am aware these funds increase my loan balance rather than my net worth.

**Weekly Study Load Logger**
20. As a student, I want to add study tasks with a course name, task name, task type, due date, estimated hours, and status, so that I can track all of my academic commitments in one place.
21. As a student, I want to log actual hours spent on each task, so that I can compare my estimated time against the time I actually invested and understand my real study load.
22. As a student, I want to see a dedicated "Upcoming Deadlines" view showing all tasks due within the next 7 days, sorted by due date, so that I can plan my week without scrolling through every task.
23. As a student, I want to update the status of a task (To Do, In Progress, Completed, Overdue), so that I can track my progress and identify tasks that have fallen behind.
24. As a student, I want to assign a priority level (High, Medium, Low) to each task, so that I can focus effort on what matters most when time is limited.
25. As a student, I want to see total logged study hours aggregated by week, so that I can understand my study load over time and compare it with my work hours and spending on the Overview page.

**Student Loan Projection Calculator**
26. As a student, I want to enter my current student loan balance, so that the projection starts from my real financial position.
27. As a student, I want to enter my expected graduation date, so that the calculator can determine how long I have left to accumulate living cost borrowing.
28. As a student, I want the calculator to automatically use my recorded Student Loan Living Costs from the Budget module to project future borrowing, so that the projection reflects my actual spending behaviour rather than a generic estimate.
29. As a student, I want to see my estimated loan balance at graduation displayed as a clear, prominent figure, so that I can understand the long-term cost of my current lifestyle at a glance.
30. As a student, I want to see a line chart showing my loan trajectory from today to my graduation date, so that I can visualise the growth of my debt over time rather than seeing just a single number.
31. As a student, I want to interact with a "What if?" slider that reduces my projected weekly living costs, so that I can see in real time how spending less would lower my graduation balance.
32. As a student, I want a clear, prominent note explaining that NZ student loans carry no interest while I remain in New Zealand, so that I understand the rules underpinning the projection.

### Scope Boundaries

**In scope:**
- Multi-page Streamlit dashboard with a dedicated Overview homepage
- Budget & Expense Tracker: income logging (with work hours), expense logging, default fixed/variable categories, category type toggle, custom categories, per-category and overall budget limits with visual utilisation indicators, weekly/monthly view toggle
- Weekly Study Load Logger: task entry, logged hours per task, upcoming 7-day deadline view, status and priority tracking, weekly hours aggregation
- Student Loan Projection Calculator: graduation balance figure, trajectory line chart, "What if?" slider, NZ interest-free note, automatic consumption of Budget living cost entries
- Overview homepage: Balance Score, week-on-week comparison cards, combined work/study/spending chart
- Load Sample Data and Clear Sample Data (NZ-realistic figures)
- SQLite local database with persistence across sessions

**Out of scope:**
- User accounts or authentication (single-user prototype only)
- Automatic bank or credit card data synchronisation
- Advanced financial planning tools (investment tracking, savings goals, complex what-if scenarios beyond the loan slider)
- Push notifications or budget alerts
- Data export or import (CSV, PDF, or other formats)
- Multi-currency support
- Integration with university LMS or external academic systems
- Automated loan repayment strategy simulations
- AI-driven or machine-learning insights
- Grade tracking

---

## 3. User Experience

### User Journey

**Demo / first visit path:**
1. User opens StudentLens in their browser via the Codespace port.
2. They land on the Overview homepage, which shows labelled empty-state placeholders.
3. They click "Load Sample Data" — the dashboard populates instantly with realistic NZ student data across all three modules.
4. The Overview page now shows: a colour-coded Balance Score, three week-on-week comparison cards (spending, work hours, study hours), and a combined chart.
5. The user navigates to the Budget module, browses income and expense entries, and explores the category budget utilisation indicators.
6. They navigate to the Study Load module, review upcoming deadlines, and browse logged hours.
7. They navigate to the Loan Projection module, view the graduation balance and trajectory chart, and interact with the "What if?" slider to explore different spending scenarios.

**Ongoing personal use path:**
1. User clicks "Clear Sample Data" and begins entering their own income, expenses, and study tasks.
2. Each week, they log work hours with income, record expenses by category, and log study sessions against tasks.
3. The Overview page automatically reflects their entries and highlights emerging patterns.
4. Budget limit indicators signal visually when spending is approaching or exceeding a set limit.
5. The upcoming deadlines view surfaces what is due this week, helping the user plan study sessions around work shifts.
6. The loan projection auto-updates as new living cost entries accumulate.

**UX expectations:**
- Every module should be immediately understandable without instructions or onboarding.
- Data entry forms should be minimal — ask only for what is necessary.
- All visualisations should be clearly labelled; no chart should require interpretation effort.
- The distinction between Student Loan Living Costs (debt) and true income should be visually reinforced, not buried in a footnote.
- Navigation between pages must feel instant with no visible loading delay.

### Acceptance Criteria

- **Overview homepage**: Balance Score, week-on-week comparison cards, and combined chart are all present and update immediately when sample data is loaded.
- **Balance Score**: Derived from a weighted formula combining budget utilisation, work hours, and study hours logged. Displayed as green (healthy), amber (moderate stress), or red (high stress).
- **Week-on-week cards**: Show the current week's value and the signed delta (e.g., +$42, −3 hrs) compared to the previous week for spending, work hours, and study hours.
- **Combined overview chart**: Displays work hours, study hours, and total variable spending on the same time axis for the current and recent weeks.
- **Load Sample Data**: Clicking the button populates all three modules with data and refreshes the Overview within 2 seconds. Data reflects realistic NZ student figures.
- **Clear Sample Data**: Removes all records from the database and returns the dashboard to empty state.
- **Budget weekly/monthly toggle**: Switching the toggle recalculates and re-renders all budget figures and charts from the same underlying entries. No data re-entry is required.
- **Budget limit indicators**: Each category with a limit set shows a visual progress bar or ring. Colour changes from green to amber at 75% utilisation and red at 100%.
- **Student Loan Living Costs distinction**: Income entries of this type are visually flagged as debt (not true income) within the Budget module — e.g., a label, badge, or distinct colour.
- **Upcoming deadlines view**: Displays all tasks with due dates within the next 7 days, sorted by due date ascending. Tasks with no upcoming due date are not shown in this view.
- **Loan projection figure**: Calculated as Current Balance + (average weekly Student Loan Living Costs from Budget module × remaining weeks to graduation). Displayed prominently.
- **Loan trajectory chart**: Renders a line from today's balance to the projected graduation balance, with time on the x-axis and loan balance on the y-axis.
- **"What if?" slider**: Moving the slider updates both the graduation balance figure and the trajectory chart in real time without a page reload.
- **NZ interest-free note**: Permanently visible on the Loan Projection page, not hidden behind a tooltip or collapsible.
- **Data persistence**: All entered data survives a full browser refresh and a Codespace restart.

---

## 4. Constraints

### Regulatory / Legal
None identified. This is a single-user local prototype with no personal data shared externally and no sensitive financial data transmitted over a network.

### Platform & Standards
- Runs as a Python Streamlit application inside a GitHub Codespace
- Accessed via browser through Codespace port forwarding — no hardcoded IP addresses
- Desktop browser only; no mobile optimisation required for the prototype
- Single-user; no concurrent access requirement

### Performance Requirements
- "Load Sample Data" must fully populate the dashboard within 2 seconds
- Navigation between pages must feel near-instant (no heavy server-side processing on each page load)
- No uptime, availability, or scalability targets (prototype environment)

### Assumptions & Risks

| Assumption | Risk if wrong |
|-----------|--------------|
| Users will enter data consistently over time for correlations to emerge | Without consistent data, the overview chart shows sparse noise rather than signal — sample data mitigates this for demos |
| NZ student figures for a Canterbury/main-centre student are representative enough for the prototype | Sample data may feel unrealistic to students in different regions or circumstances |
| The interaction between work hours, study hours, and spending is visible at weekly granularity | The relationship may only emerge over months, making the weekly chart misleading for short periods |
| A single Balance Score formula works across different student circumstances | A student working high hours by choice (not financial necessity) may be flagged as "stressed" incorrectly |
| Streamlit's layout system is sufficient for the intended dashboard design | Some visualisation or layout choices may require workarounds within Streamlit's constraints |
| The prototype runs locally in a Codespace and is not deployed externally | External deployment would introduce security, authentication, and scalability requirements not addressed here |
| NZ student loan living cost disbursements are consistent enough week-to-week to extrapolate meaningfully | If disbursements are lump-sum and irregular, the weekly average extrapolation will be inaccurate |

---

## 5. Priorities (Delivery Plan)

### Must-have (MVP)
- Overview homepage with Balance Score, week-on-week comparison cards, and combined work/study/spending chart
- Budget & Expense Tracker: income logging with work hours, expense logging, default fixed/variable categories, weekly/monthly toggle, overall budget limit with visual indicator, Student Loan Living Costs distinction
- Weekly Study Load Logger: task entry, logged hours, upcoming 7-day deadline view, status tracking
- Student Loan Projection Calculator: graduation balance figure, trajectory line chart, "What if?" slider, NZ interest-free note, automatic reading of Budget living cost data
- Load Sample Data and Clear Sample Data (NZ-realistic figures across all modules)
- SQLite local database with session persistence

### Can wait
- Per-category budget limits (overall limit is sufficient for the MVP demo; per-category adds UI complexity)
- Custom category creation and fixed/variable category toggling
- Priority field on study tasks
- Advanced Balance Score configuration or user-adjustable thresholds

### Order of work
1. **Database schema and sample data** — the foundation that all modules depend on; NZ figures defined here
2. **Budget & Expense Tracker** — the most data-rich module; establishes income and expense records that feed cross-module features
3. **Study Load Logger** — adds logged hours data that feeds the overview chart
4. **Overview homepage** — assembled from data already produced by modules above
5. **Loan Projection Calculator** — consumes Budget module living cost data; built once Budget is stable
6. **Polish** — Balance Score logic, week-on-week cards, visual refinements, Load/Clear Sample Data

---

## Further Notes

- Sample data should represent a plausible Canterbury NZ student: part-time café or retail work at approximately 15 hours per week and NZ minimum wage (~$23.15/hr); weekly rent ~$220–$250; Student Loan Living Costs ~$280/week; typical weekly spending across Food (~$80), Social (~$40), Transport (~$30), Power (~$20).
- The NZ student loan carries no interest while the borrower remains in New Zealand. The Loan Projection module assumes the student remains in NZ throughout and should state this clearly.
- This is a prototype only. All design and build decisions should optimise for clarity and demonstrability, not production scale, security hardening, or maintainability.
