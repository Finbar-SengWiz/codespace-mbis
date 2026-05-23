import streamlit as st
from datetime import date
from db import (
    add_income_entry, get_income_entries,
    add_expense, get_expense_entries,
    get_expense_categories,
)

SOURCE_TYPES = ["Part-time Work", "Allowance", "Scholarship", "Student Loan Living Costs"]


def show():
    st.title("Budget & Expenses")

    period = st.radio("View", ["Weekly", "Monthly"], horizontal=True)
    period_key = period.lower()

    st.divider()

    col_income, col_expense = st.columns(2)

    with col_income:
        st.subheader("Add Income")
        source = st.selectbox("Source", SOURCE_TYPES)
        with st.form("income_form", clear_on_submit=True):
            amount = st.number_input("Amount ($)", min_value=0.01, step=0.01, format="%.2f")
            entry_date = st.date_input("Date", value=date.today())
            work_hours = None
            if source == "Part-time Work":
                work_hours = st.number_input("Work Hours", min_value=0.0, step=0.5, format="%.1f")
            submitted = st.form_submit_button("Add Income")
            if submitted:
                add_income_entry(
                    source_type=source,
                    amount=amount,
                    date=entry_date.isoformat(),
                    work_hours=work_hours if source == "Part-time Work" else None,
                )
                st.success("Income entry added.")

    with col_expense:
        st.subheader("Add Expense")
        categories = get_expense_categories()
        category_names = [c["name"] for c in categories]
        with st.form("expense_form", clear_on_submit=True):
            category = st.selectbox("Category", category_names)
            amount_exp = st.number_input("Amount ($)", min_value=0.01, step=0.01, format="%.2f", key="exp_amount")
            entry_date_exp = st.date_input("Date", value=date.today(), key="exp_date")
            submitted_exp = st.form_submit_button("Add Expense")
            if submitted_exp:
                add_expense(
                    category_name=category,
                    amount=amount_exp,
                    date=entry_date_exp.isoformat(),
                )
                st.success("Expense entry added.")

    st.divider()

    _show_income_table(period_key)
    _show_expense_table(period_key)


def _show_income_table(period):
    st.subheader("Income Entries")
    entries = get_income_entries(period=period)
    if not entries:
        st.caption("No income entries for this period.")
        return

    for e in entries:
        is_loan = e["source_type"] == "Student Loan Living Costs"
        badge = " :red[— DEBT, not income]" if is_loan else ""
        hours_str = f"  |  {e['work_hours']:.1f} hrs worked" if e["work_hours"] else ""
        st.markdown(
            f"**{e['date']}** — {e['source_type']}{badge}  |  **${e['amount']:.2f}**{hours_str}"
        )


def _show_expense_table(period):
    st.subheader("Expense Entries")
    entries = get_expense_entries(period=period)
    if not entries:
        st.caption("No expense entries for this period.")
        return

    for e in entries:
        st.markdown(f"**{e['date']}** — {e['category_name']}  |  **${e['amount']:.2f}**")
