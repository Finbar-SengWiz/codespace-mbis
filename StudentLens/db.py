import os
import sqlite3
from datetime import date, timedelta

_HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DB_PATH = os.path.join(_HERE, "data", "studentlens.db")


def init_db(db_path=DEFAULT_DB_PATH):
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS income_entries (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            source_type TEXT    NOT NULL,
            amount      REAL    NOT NULL,
            date        TEXT    NOT NULL,
            work_hours  REAL
        );
        CREATE TABLE IF NOT EXISTS expense_entries (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT    NOT NULL,
            amount        REAL    NOT NULL,
            date          TEXT    NOT NULL
        );
        CREATE TABLE IF NOT EXISTS expense_categories (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT    NOT NULL UNIQUE,
            category_type TEXT    NOT NULL,
            budget_limit  REAL
        );
        CREATE TABLE IF NOT EXISTS study_tasks (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            course          TEXT    NOT NULL,
            task_name       TEXT    NOT NULL,
            task_type       TEXT    NOT NULL,
            due_date        TEXT,
            estimated_hours REAL    NOT NULL DEFAULT 0,
            logged_hours    REAL    NOT NULL DEFAULT 0,
            status          TEXT    NOT NULL DEFAULT 'To Do',
            priority        TEXT    NOT NULL DEFAULT 'None'
        );
        CREATE TABLE IF NOT EXISTS app_settings (
            key   TEXT PRIMARY KEY,
            value TEXT
        );
    """)
    _seed_default_categories(conn)
    conn.commit()
    conn.close()


def _seed_default_categories(conn):
    defaults = [
        ("Rent", "fixed"),
        ("Tuition", "fixed"),
        ("Transport", "fixed"),
        ("Food", "variable"),
        ("Social", "variable"),
        ("Entertainment", "variable"),
        ("Power", "variable"),
    ]
    conn.executemany(
        "INSERT OR IGNORE INTO expense_categories (name, category_type) VALUES (?, ?)",
        defaults,
    )


def add_income_entry(db_path=DEFAULT_DB_PATH, source_type=None, amount=None, date=None, work_hours=None):
    conn = sqlite3.connect(db_path)
    conn.execute(
        "INSERT INTO income_entries (source_type, amount, date, work_hours) VALUES (?, ?, ?, ?)",
        (source_type, amount, date, work_hours),
    )
    conn.commit()
    conn.close()


def get_income_entries(db_path=DEFAULT_DB_PATH, period=None):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    if period == "weekly":
        rows = conn.execute(
            "SELECT * FROM income_entries WHERE strftime('%Y-%W', date) = strftime('%Y-%W', 'now') ORDER BY date DESC"
        ).fetchall()
    elif period == "monthly":
        rows = conn.execute(
            "SELECT * FROM income_entries WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now') ORDER BY date DESC"
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM income_entries ORDER BY date DESC").fetchall()
    conn.close()
    return [dict(row) for row in rows]


def add_expense(db_path=DEFAULT_DB_PATH, category_name=None, amount=None, date=None):
    conn = sqlite3.connect(db_path)
    conn.execute(
        "INSERT INTO expense_entries (category_name, amount, date) VALUES (?, ?, ?)",
        (category_name, amount, date),
    )
    conn.commit()
    conn.close()


def get_expense_entries(db_path=DEFAULT_DB_PATH, period=None):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    if period == "weekly":
        rows = conn.execute(
            "SELECT * FROM expense_entries WHERE strftime('%Y-%W', date) = strftime('%Y-%W', 'now') ORDER BY date DESC"
        ).fetchall()
    elif period == "monthly":
        rows = conn.execute(
            "SELECT * FROM expense_entries WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now') ORDER BY date DESC"
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM expense_entries ORDER BY date DESC").fetchall()
    conn.close()
    return [dict(row) for row in rows]


def add_study_task(db_path=DEFAULT_DB_PATH, course=None, task_name=None, task_type=None,
                   due_date=None, estimated_hours=0.0, logged_hours=0.0,
                   status="To Do", priority="None"):
    conn = sqlite3.connect(db_path)
    conn.execute(
        """INSERT INTO study_tasks
           (course, task_name, task_type, due_date, estimated_hours, logged_hours, status, priority)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (course, task_name, task_type, due_date, estimated_hours, logged_hours, status, priority),
    )
    conn.commit()
    conn.close()


def get_study_tasks(db_path=DEFAULT_DB_PATH):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT * FROM study_tasks ORDER BY due_date IS NULL, due_date ASC"
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def update_task_status(db_path=DEFAULT_DB_PATH, task_id=None, new_status=None):
    conn = sqlite3.connect(db_path)
    conn.execute("UPDATE study_tasks SET status = ? WHERE id = ?", (new_status, task_id))
    conn.commit()
    conn.close()


def log_task_hours(db_path=DEFAULT_DB_PATH, task_id=None, hours=0.0):
    conn = sqlite3.connect(db_path)
    conn.execute(
        "UPDATE study_tasks SET logged_hours = logged_hours + ? WHERE id = ?",
        (hours, task_id),
    )
    conn.commit()
    conn.close()


def get_upcoming_tasks(db_path=DEFAULT_DB_PATH):
    today = date.today().isoformat()
    cutoff = (date.today() + timedelta(days=7)).isoformat()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT * FROM study_tasks WHERE due_date >= ? AND due_date <= ? ORDER BY due_date ASC",
        (today, cutoff),
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_weekly_study_hours(db_path=DEFAULT_DB_PATH):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        """SELECT strftime('%Y-%W', due_date) AS week, SUM(logged_hours) AS hours
           FROM study_tasks
           WHERE due_date IS NOT NULL
           GROUP BY week
           ORDER BY week ASC"""
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_weekly_work_hours(db_path=DEFAULT_DB_PATH):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        """SELECT strftime('%Y-%W', date) AS week, SUM(work_hours) AS hours
           FROM income_entries
           WHERE source_type = 'Part-time Work' AND work_hours IS NOT NULL
           GROUP BY week
           ORDER BY week ASC"""
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_weekly_variable_spending(db_path=DEFAULT_DB_PATH):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        """SELECT strftime('%Y-%W', e.date) AS week, SUM(e.amount) AS amount
           FROM expense_entries e
           JOIN expense_categories c ON e.category_name = c.name
           WHERE c.category_type = 'variable'
           GROUP BY week
           ORDER BY week ASC"""
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def set_app_setting(db_path=DEFAULT_DB_PATH, key=None, value=None):
    conn = sqlite3.connect(db_path)
    conn.execute(
        "INSERT OR REPLACE INTO app_settings (key, value) VALUES (?, ?)",
        (key, value),
    )
    conn.commit()
    conn.close()


def get_app_setting(db_path=DEFAULT_DB_PATH, key=None):
    conn = sqlite3.connect(db_path)
    row = conn.execute("SELECT value FROM app_settings WHERE key = ?", (key,)).fetchone()
    conn.close()
    return row[0] if row else None


def get_avg_weekly_living_costs(db_path=DEFAULT_DB_PATH):
    conn = sqlite3.connect(db_path)
    row = conn.execute(
        """SELECT AVG(weekly_total) FROM (
               SELECT SUM(amount) AS weekly_total
               FROM income_entries
               WHERE source_type = 'Student Loan Living Costs'
               GROUP BY strftime('%Y-%W', date)
           )"""
    ).fetchone()
    conn.close()
    if row and row[0] is not None:
        return round(row[0], 2)
    return 280.0


def load_sample_data(db_path=DEFAULT_DB_PATH):
    today = date.today()
    conn = sqlite3.connect(db_path)

    # --- Income: 8 weeks of Part-time Work + Student Loan Living Costs ---
    weekly_work = [
        (15.0, 347.25), (10.0, 231.50), (15.0, 347.25), (15.0, 347.25),
        (11.0, 254.65), (15.0, 347.25), (15.0, 347.25), (10.0, 231.50),
    ]
    for i, (hrs, pay) in enumerate(weekly_work):
        d = (today - timedelta(weeks=8 - i)).isoformat()
        conn.execute(
            "INSERT INTO income_entries (source_type, amount, date, work_hours) VALUES (?,?,?,?)",
            ("Part-time Work", pay, d, hrs),
        )
        conn.execute(
            "INSERT INTO income_entries (source_type, amount, date, work_hours) VALUES (?,?,?,?)",
            ("Student Loan Living Costs", 280.00, d, None),
        )

    # --- Expenses: 8 weeks of realistic NZ student spending ---
    weekly_expenses = [
        [("Rent", 235.00), ("Food", 82.50), ("Transport", 30.00), ("Power", 20.00), ("Social", 38.00)],
        [("Rent", 235.00), ("Food", 76.00), ("Transport", 30.00), ("Power", 20.00), ("Entertainment", 28.00)],
        [("Rent", 235.00), ("Food", 88.00), ("Transport", 30.00), ("Power", 20.00), ("Social", 45.00)],
        [("Rent", 235.00), ("Food", 79.50), ("Transport", 30.00), ("Power", 20.00), ("Social", 32.00)],
        [("Rent", 235.00), ("Food", 91.00), ("Transport", 30.00), ("Power", 20.00), ("Entertainment", 35.00)],
        [("Rent", 235.00), ("Food", 74.00), ("Transport", 30.00), ("Power", 20.00), ("Social", 41.00)],
        [("Rent", 235.00), ("Food", 85.00), ("Transport", 30.00), ("Power", 20.00), ("Social", 36.00)],
        [("Rent", 235.00), ("Food", 80.00), ("Transport", 30.00), ("Power", 20.00), ("Entertainment", 22.00)],
    ]
    for i, week_exps in enumerate(weekly_expenses):
        d = (today - timedelta(weeks=8 - i)).isoformat()
        for cat, amt in week_exps:
            conn.execute(
                "INSERT INTO expense_entries (category_name, amount, date) VALUES (?,?,?)",
                (cat, amt, d),
            )

    # --- Study tasks: 5 tasks across 3 courses ---
    tasks = [
        ("BSNS101", "Market Analysis Report", "Assignment",
         (today + timedelta(days=5)).isoformat(),  3.0, 0.0, "In Progress", "High"),
        ("BSNS101", "Weekly Reading — Ch 4 & 5", "Reading",
         (today + timedelta(days=2)).isoformat(),  1.5, 0.0, "To Do",       "Medium"),
        ("ECON201", "Consumer Behaviour Essay",   "Assignment",
         (today + timedelta(days=14)).isoformat(), 6.0, 0.0, "To Do",       "High"),
        ("ECON201", "Mid-term Exam Revision",     "Exam",
         (today + timedelta(days=21)).isoformat(), 8.0, 0.0, "To Do",       "High"),
        ("MGMT301", "Group Project Presentation", "Assignment",
         (today + timedelta(days=30)).isoformat(), 5.0, 0.0, "To Do",       "Medium"),
    ]
    conn.executemany(
        """INSERT INTO study_tasks
           (course, task_name, task_type, due_date, estimated_hours, logged_hours, status, priority)
           VALUES (?,?,?,?,?,?,?,?)""",
        tasks,
    )

    # --- Loan settings ---
    grad_date = (today + timedelta(weeks=78)).isoformat()
    conn.execute(
        "INSERT OR REPLACE INTO app_settings (key, value) VALUES (?, ?)",
        ("loan_balance", "18500.00"),
    )
    conn.execute(
        "INSERT OR REPLACE INTO app_settings (key, value) VALUES (?, ?)",
        ("graduation_date", grad_date),
    )

    conn.commit()
    conn.close()


def clear_sample_data(db_path=DEFAULT_DB_PATH):
    conn = sqlite3.connect(db_path)
    for tbl in ["income_entries", "expense_entries", "study_tasks", "app_settings"]:
        conn.execute(f"DELETE FROM {tbl}")
    conn.commit()
    conn.close()


def get_expense_categories(db_path=DEFAULT_DB_PATH):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM expense_categories ORDER BY id").fetchall()
    conn.close()
    return [dict(row) for row in rows]
