import streamlit as st
import pandas as pd
from datetime import date, timedelta
from db import get_app_setting, set_app_setting, get_avg_weekly_living_costs
from calculations import project_loan_balance, loan_trajectory

FALLBACK_WEEKLY_COSTS = 280.0
MIN_GRAD_DATE = date.today() + timedelta(weeks=4)


def show():
    st.title("Loan Projection")

    st.info(
        "NZ student loans carry **no interest** while you remain in New Zealand. "
        "This projection assumes you stay in NZ until graduation."
    )

    st.subheader("Your Details")
    col1, col2 = st.columns(2)

    with col1:
        saved_balance = get_app_setting(key="loan_balance")
        default_balance = float(saved_balance) if saved_balance else 18000.0
        balance = st.number_input(
            "Current Loan Balance ($)",
            min_value=0.0, value=default_balance, step=100.0, format="%.2f"
        )

    with col2:
        saved_grad = get_app_setting(key="graduation_date")
        default_grad = date.fromisoformat(saved_grad) if saved_grad else MIN_GRAD_DATE
        grad_date = st.date_input(
            "Expected Graduation Date",
            value=default_grad,
            min_value=date.today() + timedelta(days=1),
        )

    if balance != default_balance:
        set_app_setting(key="loan_balance", value=str(balance))
    if grad_date != default_grad:
        set_app_setting(key="graduation_date", value=grad_date.isoformat())

    st.divider()

    avg_costs = get_avg_weekly_living_costs()
    using_fallback = avg_costs == FALLBACK_WEEKLY_COSTS and get_avg_weekly_living_costs() == FALLBACK_WEEKLY_COSTS

    if using_fallback:
        st.caption(
            f"No Student Loan Living Costs recorded in Budget yet. "
            f"Using default estimate of ${FALLBACK_WEEKLY_COSTS:.0f}/week."
        )

    st.subheader("What if? — Adjust Weekly Living Costs")
    adjusted_costs = st.slider(
        "Projected weekly living costs ($)",
        min_value=0, max_value=320, value=int(avg_costs), step=10,
        help="Move the slider to see how reducing your living costs affects your graduation balance."
    )

    remaining_weeks = max((grad_date - date.today()).days / 7, 0)
    projected = project_loan_balance(balance, grad_date, adjusted_costs)

    st.divider()

    col_fig, col_chart = st.columns([1, 2])

    with col_fig:
        st.metric(
            label="Estimated Loan Balance at Graduation",
            value=f"${projected:,.0f}",
            delta=f"{projected - balance:+,.0f} added over {remaining_weeks:.0f} weeks",
            delta_color="inverse",
        )

    with col_chart:
        points = loan_trajectory(balance, grad_date, adjusted_costs)
        df = pd.DataFrame(points, columns=["Date", "Balance"])
        df["Date"] = pd.to_datetime(df["Date"])
        st.line_chart(df.set_index("Date")["Balance"], use_container_width=True)
