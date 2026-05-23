from datetime import date, timedelta


def balance_score(budget_util, work_hours, study_hours):
    util_norm  = min(budget_util, 1.0)
    work_norm  = min(work_hours / 15, 1.0)
    study_norm = 1 - min(study_hours / 20, 1.0)
    score = util_norm * 0.4 + work_norm * 0.3 + study_norm * 0.3
    if score < 0.5:
        return score, "green"
    elif score < 0.75:
        return score, "amber"
    else:
        return score, "red"


def project_loan_balance(current_balance, graduation_date, weekly_living_costs):
    remaining_weeks = (graduation_date - date.today()).days / 7
    return current_balance + weekly_living_costs * remaining_weeks


def loan_trajectory(current_balance, graduation_date, weekly_living_costs):
    points = []
    today = date.today()
    total_days = (graduation_date - today).days
    weeks = max(int(total_days / 7), 1)
    for i in range(weeks + 1):
        point_date = today + timedelta(weeks=i)
        balance = current_balance + weekly_living_costs * i
        points.append((point_date, balance))
    return points
