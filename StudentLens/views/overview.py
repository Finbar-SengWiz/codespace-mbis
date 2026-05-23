import streamlit as st
import pandas as pd
from datetime import date
from db import (
    get_weekly_work_hours, get_weekly_variable_spending,
    get_weekly_study_hours, get_app_setting,
    load_sample_data, clear_sample_data,
)
from calculations import balance_score

SCORE_COLOURS = {"green": "🟢", "amber": "🟡", "red": "🔴"}
SCORE_LABELS  = {"green": "Healthy", "amber": "Moderate Pressure", "red": "High Pressure"}


def show():
    st.title("Overview")

    _show_sample_data_buttons()
    st.divider()
    _show_balance_score()
    st.divider()
    _show_week_on_week_cards()
    st.divider()
    _show_combined_chart()


# ── Sample data buttons ───────────────────────────────────────────────────────

def _show_sample_data_buttons():
    col1, col2, _ = st.columns([1, 1, 3])
    with col1:
        if st.button("Load Sample Data", type="primary", use_container_width=True):
            load_sample_data()
            st.rerun()
    with col2:
        if st.button("Clear All Data", type="secondary", use_container_width=True):
            clear_sample_data()
            st.rerun()


# ── Balance Score ─────────────────────────────────────────────────────────────

def _show_balance_score():
    this_week = date.today().strftime("%Y-%W")

    work_data    = get_weekly_work_hours()
    study_data   = get_weekly_study_hours()
    spend_data   = get_weekly_variable_spending()

    this_work  = next((w["hours"]  for w in work_data  if w["week"] == this_week), 0.0)
    this_study = next((w["hours"]  for w in study_data if w["week"] == this_week), 0.0)
    this_spend = next((w["amount"] for w in spend_data if w["week"] == this_week), 0.0)

    overall_limit_raw = get_app_setting(key="overall_budget_limit")
    overall_limit = float(overall_limit_raw) if overall_limit_raw else None
    budget_util = (this_spend / overall_limit) if overall_limit else 0.0

    score, colour = balance_score(budget_util, this_work, this_study)

    st.subheader("Wellbeing Balance Score — Academic & Financial")
    col, _ = st.columns([1, 2])
    with col:
        st.metric(
            label=f"{SCORE_COLOURS[colour]} {SCORE_LABELS[colour]}",
            value=f"{score:.0%}",
            help="Composite of budget utilisation (40%), work hours (30%), and study hours (30%). Lower is healthier.",
        )
    if not overall_limit:
        st.caption("Set an overall budget limit in Budget & Expenses to include spending in this score.")


# ── Week-on-week cards ────────────────────────────────────────────────────────

def _show_week_on_week_cards():
    st.subheader("This Week vs Last Week")

    this_week = date.today().strftime("%Y-%W")
    all_weeks = sorted({w["week"] for data in [
        get_weekly_work_hours(), get_weekly_variable_spending(), get_weekly_study_hours()
    ] for w in data})
    prev_week = all_weeks[all_weeks.index(this_week) - 1] if this_week in all_weeks and all_weeks.index(this_week) > 0 else None

    work_data  = {w["week"]: w["hours"]  for w in get_weekly_work_hours()}
    study_data = {w["week"]: w["hours"]  for w in get_weekly_study_hours()}
    spend_data = {w["week"]: w["amount"] for w in get_weekly_variable_spending()}

    this_work  = work_data.get(this_week, 0.0)
    this_study = study_data.get(this_week, 0.0)
    this_spend = spend_data.get(this_week, 0.0)
    prev_work  = work_data.get(prev_week, 0.0) if prev_week else None
    prev_study = study_data.get(prev_week, 0.0) if prev_week else None
    prev_spend = spend_data.get(prev_week, 0.0) if prev_week else None

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Variable Spending", f"${this_spend:.0f}",
                  delta=f"${this_spend - prev_spend:+.0f} vs last week" if prev_spend is not None else None,
                  delta_color="inverse")
    with col2:
        st.metric("Work Hours", f"{this_work:.1f} hrs",
                  delta=f"{this_work - prev_work:+.1f} hrs vs last week" if prev_work is not None else None,
                  delta_color="inverse")
    with col3:
        st.metric("Study Hours", f"{this_study:.1f} hrs",
                  delta=f"{this_study - prev_study:+.1f} hrs vs last week" if prev_study is not None else None)


# ── Combined chart ────────────────────────────────────────────────────────────

def _show_combined_chart():
    st.subheader("Weekly Overview — Work, Study & Spending")

    work_data  = {w["week"]: w["hours"]  for w in get_weekly_work_hours()}
    study_data = {w["week"]: w["hours"]  for w in get_weekly_study_hours()}
    spend_data = {w["week"]: w["amount"] for w in get_weekly_variable_spending()}

    all_weeks = sorted(set(work_data) | set(study_data) | set(spend_data))

    if not all_weeks:
        st.caption("No data yet. Load sample data or start entering your own records.")
        return

    df = pd.DataFrame({
        "Week": all_weeks,
        "Work Hours": [work_data.get(w, 0.0) for w in all_weeks],
        "Study Hours": [study_data.get(w, 0.0) for w in all_weeks],
        "Variable Spending ($)": [spend_data.get(w, 0.0) for w in all_weeks],
    }).set_index("Week")

    st.line_chart(df, use_container_width=True)
