import sqlite3
import pytest
from datetime import date, timedelta
from db import (
    init_db, get_expense_categories,
    add_income_entry, get_income_entries,
    add_expense, get_expense_entries,
    add_study_task, get_study_tasks,
    update_task_status, log_task_hours,
    get_upcoming_tasks, get_weekly_study_hours,
    set_app_setting, get_app_setting,
    get_avg_weekly_living_costs,
    get_weekly_work_hours, get_weekly_variable_spending,
    load_sample_data, clear_sample_data,
)


@pytest.fixture
def db_path(tmp_path):
    path = str(tmp_path / "test.db")
    init_db(path)
    return path


EXPECTED_FIXED = {"Rent", "Tuition", "Transport"}
EXPECTED_VARIABLE = {"Food", "Social", "Entertainment", "Power"}
EXPECTED_ALL = EXPECTED_FIXED | EXPECTED_VARIABLE


def test_tables_exist(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = {row[0] for row in cursor.fetchall()}
    conn.close()
    assert "income_entries" in tables
    assert "expense_entries" in tables
    assert "expense_categories" in tables
    assert "study_tasks" in tables
    assert "app_settings" in tables


def test_default_categories_loaded(db_path):
    categories = get_expense_categories(db_path)
    names = {c["name"] for c in categories}
    assert names == EXPECTED_ALL

    fixed = {c["name"] for c in categories if c["category_type"] == "fixed"}
    variable = {c["name"] for c in categories if c["category_type"] == "variable"}
    assert fixed == EXPECTED_FIXED
    assert variable == EXPECTED_VARIABLE


def test_no_duplicate_categories(db_path):
    init_db(db_path)  # second call on the same db
    categories = get_expense_categories(db_path)
    assert len(categories) == len(EXPECTED_ALL)


# ── Phase 2: Budget data entry ────────────────────────────────────────────────

def test_add_and_get_income_entry(db_path):
    add_income_entry(db_path, "Allowance", 100.00, "2026-05-20")
    entries = get_income_entries(db_path)
    assert len(entries) == 1
    e = entries[0]
    assert e["source_type"] == "Allowance"
    assert e["amount"] == 100.00
    assert e["date"] == "2026-05-20"
    assert e["work_hours"] is None


def test_work_hours_stored_for_part_time_work(db_path):
    add_income_entry(db_path, "Part-time Work", 347.25, "2026-05-20", work_hours=15.0)
    entries = get_income_entries(db_path)
    assert entries[0]["work_hours"] == 15.0


def test_add_and_get_expense_entry(db_path):
    add_expense(db_path, "Food", 25.50, "2026-05-20")
    entries = get_expense_entries(db_path)
    assert len(entries) == 1
    e = entries[0]
    assert e["category_name"] == "Food"
    assert e["amount"] == 25.50
    assert e["date"] == "2026-05-20"


def test_weekly_filter(db_path):
    today = date.today().isoformat()
    old = (date.today() - timedelta(weeks=2)).isoformat()
    add_income_entry(db_path, "Allowance", 100.00, today)
    add_income_entry(db_path, "Allowance", 50.00, old)
    entries = get_income_entries(db_path, period="weekly")
    assert len(entries) == 1
    assert entries[0]["amount"] == 100.00


def test_monthly_filter(db_path):
    today = date.today().isoformat()
    old = (date.today() - timedelta(days=40)).isoformat()
    add_expense(db_path, "Food", 50.00, today)
    add_expense(db_path, "Food", 30.00, old)
    entries = get_expense_entries(db_path, period="monthly")
    assert len(entries) == 1
    assert entries[0]["amount"] == 50.00


# ── Phase 3: Study Load Logger ────────────────────────────────────────────────

def test_add_and_get_study_task(db_path):
    add_study_task(db_path, course="BSNS101", task_name="Case Study",
                   task_type="Assignment", due_date="2026-06-01",
                   estimated_hours=4.0)
    tasks = get_study_tasks(db_path)
    assert len(tasks) == 1
    t = tasks[0]
    assert t["course"] == "BSNS101"
    assert t["task_name"] == "Case Study"
    assert t["task_type"] == "Assignment"
    assert t["due_date"] == "2026-06-01"
    assert t["estimated_hours"] == 4.0
    assert t["logged_hours"] == 0.0
    assert t["status"] == "To Do"
    assert t["priority"] == "None"


def test_update_task_status(db_path):
    add_study_task(db_path, course="BSNS101", task_name="Reading",
                   task_type="Reading", status="To Do")
    task_id = get_study_tasks(db_path)[0]["id"]
    update_task_status(db_path, task_id=task_id, new_status="In Progress")
    assert get_study_tasks(db_path)[0]["status"] == "In Progress"


def test_log_task_hours(db_path):
    add_study_task(db_path, course="BSNS101", task_name="Lab",
                   task_type="Lab", logged_hours=1.0)
    task_id = get_study_tasks(db_path)[0]["id"]
    log_task_hours(db_path, task_id=task_id, hours=2.5)
    assert get_study_tasks(db_path)[0]["logged_hours"] == 3.5


def test_upcoming_tasks_within_7_days(db_path):
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    in_3_days = (date.today() + timedelta(days=3)).isoformat()
    in_10_days = (date.today() + timedelta(days=10)).isoformat()
    add_study_task(db_path, course="A", task_name="Soon", task_type="Assignment", due_date=tomorrow)
    add_study_task(db_path, course="A", task_name="Also soon", task_type="Reading", due_date=in_3_days)
    add_study_task(db_path, course="A", task_name="Far", task_type="Exam", due_date=in_10_days)
    add_study_task(db_path, course="A", task_name="No date", task_type="Other")
    upcoming = get_upcoming_tasks(db_path)
    assert len(upcoming) == 2
    assert upcoming[0]["due_date"] == tomorrow
    assert upcoming[1]["due_date"] == in_3_days


def test_weekly_study_hours(db_path):
    this_week_date = date.today().isoformat()
    add_study_task(db_path, course="BSNS101", task_name="T1",
                   task_type="Assignment", due_date=this_week_date, logged_hours=3.0)
    add_study_task(db_path, course="BSNS102", task_name="T2",
                   task_type="Reading", due_date=this_week_date, logged_hours=1.5)
    weekly = get_weekly_study_hours(db_path)
    this_week_key = date.today().strftime("%Y-%W")
    entry = next((w for w in weekly if w["week"] == this_week_key), None)
    assert entry is not None
    assert entry["hours"] == 4.5


# ── Phase 4: Loan Projection db functions ─────────────────────────────────────

def test_app_setting_roundtrip(db_path):
    set_app_setting(db_path, "loan_balance", "18000.00")
    assert get_app_setting(db_path, "loan_balance") == "18000.00"


def test_app_setting_missing_key_returns_none(db_path):
    assert get_app_setting(db_path, "nonexistent_key") is None


def test_get_avg_weekly_living_costs(db_path):
    # Week 1: two entries totalling $280
    add_income_entry(db_path, "Student Loan Living Costs", 140.00, "2026-05-04")
    add_income_entry(db_path, "Student Loan Living Costs", 140.00, "2026-05-06")
    # Week 2: one entry of $280
    add_income_entry(db_path, "Student Loan Living Costs", 280.00, "2026-05-11")
    # Other income types should be ignored
    add_income_entry(db_path, "Part-time Work", 500.00, "2026-05-04", work_hours=15.0)
    avg = get_avg_weekly_living_costs(db_path)
    assert avg == 280.0


# ── Phase 5: Overview db functions ────────────────────────────────────────────

def test_get_weekly_work_hours(db_path):
    add_income_entry(db_path, "Part-time Work", 347.25, "2026-05-05", work_hours=15.0)
    add_income_entry(db_path, "Part-time Work", 231.50, "2026-05-12", work_hours=10.0)
    # Non-work income should not contribute
    add_income_entry(db_path, "Allowance", 50.00, "2026-05-05")
    weekly = get_weekly_work_hours(db_path)
    assert len(weekly) == 2
    assert weekly[0]["hours"] == 15.0
    assert weekly[1]["hours"] == 10.0


def test_get_weekly_variable_spending(db_path):
    # Variable: Food and Social
    add_expense(db_path, "Food", 40.00, "2026-05-05")
    add_expense(db_path, "Social", 25.00, "2026-05-06")
    # Fixed: Rent — should be excluded
    add_expense(db_path, "Rent", 235.00, "2026-05-05")
    weekly = get_weekly_variable_spending(db_path)
    assert len(weekly) == 1
    assert weekly[0]["amount"] == 65.00


# ── Phase 6: Sample data ──────────────────────────────────────────────────────

def test_load_sample_data_counts(tmp_path):
    path = str(tmp_path / "sample.db")
    init_db(path)
    load_sample_data(path)
    conn = sqlite3.connect(path)
    counts = {
        tbl: conn.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]
        for tbl in ["income_entries", "expense_entries", "study_tasks"]
    }
    conn.close()
    assert counts["income_entries"] >= 12
    assert counts["expense_entries"] >= 24
    assert counts["study_tasks"] >= 4


def test_clear_sample_data(tmp_path):
    path = str(tmp_path / "clear.db")
    init_db(path)
    load_sample_data(path)
    clear_sample_data(path)
    conn = sqlite3.connect(path)
    for tbl in ["income_entries", "expense_entries", "study_tasks", "app_settings"]:
        count = conn.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]
        assert count == 0, f"{tbl} should be empty after clear"
    conn.close()


def test_cross_module_consistency(tmp_path):
    path = str(tmp_path / "cross.db")
    init_db(path)
    load_sample_data(path)
    # Compute expected average manually
    conn = sqlite3.connect(path)
    row = conn.execute(
        """SELECT AVG(weekly_total) FROM (
               SELECT SUM(amount) AS weekly_total
               FROM income_entries
               WHERE source_type = 'Student Loan Living Costs'
               GROUP BY strftime('%Y-%W', date)
           )"""
    ).fetchone()
    conn.close()
    expected = round(row[0], 2) if row and row[0] else 280.0
    assert get_avg_weekly_living_costs(path) == expected
