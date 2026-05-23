import streamlit as st
from db import init_db
import views.overview as overview
import views.budget as budget
import views.study as study
import views.loan as loan

st.set_page_config(page_title="StudentLens", layout="wide")

init_db()

pg = st.navigation(
    [
        st.Page(overview.show, title="Overview", icon="🏠", url_path="", default=True),
        st.Page(budget.show, title="Budget & Expenses", icon="💰", url_path="budget"),
        st.Page(study.show, title="Study Load", icon="📚", url_path="study"),
        st.Page(loan.show, title="Loan Projection", icon="🎓", url_path="loan"),
    ]
)
pg.run()
