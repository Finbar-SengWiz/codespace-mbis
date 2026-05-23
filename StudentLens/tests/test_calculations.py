from datetime import date, timedelta
from calculations import project_loan_balance, loan_trajectory, balance_score


def test_project_loan_balance():
    # 10 weeks remaining, $280/week → adds $2,800 to $18,000 balance
    grad_date = date.today() + timedelta(weeks=10)
    result = project_loan_balance(18000.0, grad_date, 280.0)
    assert result == 18000.0 + 280.0 * 10


def test_loan_trajectory_endpoints():
    grad_date = date.today() + timedelta(weeks=4)
    points = loan_trajectory(18000.0, grad_date, 280.0)
    # First point is today's balance
    assert points[0][1] == 18000.0
    # Last point matches the standalone projection
    expected_final = project_loan_balance(18000.0, grad_date, 280.0)
    assert abs(points[-1][1] - expected_final) < 1.0
    # Points are weekly — at least 4 steps for a 4-week window
    assert len(points) >= 4


# ── Phase 5: Balance Score ─────────────────────────────────────────────────────

def test_balance_score_green():
    # Low budget use, low work hours, healthy study hours → green
    score, colour = balance_score(budget_util=0.2, work_hours=5, study_hours=18)
    assert colour == "green"
    assert score < 0.5


def test_balance_score_amber():
    # Moderate pressure across all three factors → amber
    score, colour = balance_score(budget_util=0.7, work_hours=12, study_hours=10)
    assert colour == "amber"
    assert 0.5 <= score < 0.75


def test_balance_score_red():
    # High budget use, high work hours, very low study → red
    score, colour = balance_score(budget_util=1.0, work_hours=25, study_hours=2)
    assert colour == "red"
    assert score >= 0.75
