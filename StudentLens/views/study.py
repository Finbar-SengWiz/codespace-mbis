import streamlit as st
from datetime import date
from db import add_study_task, get_study_tasks, update_task_status, log_task_hours, get_upcoming_tasks

TASK_TYPES = ["Assignment", "Exam", "Reading", "Lab", "Other"]
STATUSES = ["To Do", "In Progress", "Completed", "Overdue"]
PRIORITIES = ["None", "Low", "Medium", "High"]


def show():
    st.title("Study Load")

    _show_upcoming_deadlines()
    st.divider()
    _show_add_task_form()
    st.divider()
    _show_task_list()


def _show_upcoming_deadlines():
    st.subheader("Upcoming Deadlines (next 7 days)")
    tasks = get_upcoming_tasks()
    if not tasks:
        st.caption("No tasks due in the next 7 days.")
        return
    for t in tasks:
        priority_badge = f" [{t['priority']}]" if t["priority"] != "None" else ""
        st.markdown(
            f"**{t['due_date']}** — {t['course']}: {t['task_name']}{priority_badge}  "
            f"| _{t['status']}_ | {t['logged_hours']:.1f}/{t['estimated_hours']:.1f} hrs"
        )


def _show_add_task_form():
    st.subheader("Add Task")
    with st.form("task_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            course = st.text_input("Course")
            task_name = st.text_input("Task Name")
            task_type = st.selectbox("Task Type", TASK_TYPES)
            priority = st.selectbox("Priority", PRIORITIES)
        with col2:
            due_date = st.date_input("Due Date (optional)", value=None)
            estimated_hours = st.number_input("Estimated Hours", min_value=0.0, step=0.5, format="%.1f")
            status = st.selectbox("Status", STATUSES)
        submitted = st.form_submit_button("Add Task")
        if submitted and course and task_name:
            add_study_task(
                course=course,
                task_name=task_name,
                task_type=task_type,
                due_date=due_date.isoformat() if due_date else None,
                estimated_hours=estimated_hours,
                status=status,
                priority=priority,
            )
            st.rerun()
        elif submitted:
            st.warning("Course and Task Name are required.")


def _show_task_list():
    st.subheader("All Tasks")
    tasks = get_study_tasks()
    if not tasks:
        st.caption("No tasks yet.")
        return

    for t in tasks:
        with st.expander(f"{t['course']} — {t['task_name']} ({t['status']})"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Type:** {t['task_type']}  |  **Priority:** {t['priority']}")
                st.markdown(f"**Due:** {t['due_date'] or 'No date'}  |  **Hours:** {t['logged_hours']:.1f} logged / {t['estimated_hours']:.1f} estimated")
            with col2:
                new_status = st.selectbox(
                    "Update Status", STATUSES,
                    index=STATUSES.index(t["status"]),
                    key=f"status_{t['id']}"
                )
                if new_status != t["status"]:
                    update_task_status(task_id=t["id"], new_status=new_status)
                    st.rerun()

                with st.form(f"log_hours_{t['id']}", clear_on_submit=True):
                    extra = st.number_input("Log Hours", min_value=0.0, step=0.5, format="%.1f", key=f"log_{t['id']}")
                    if st.form_submit_button("Log"):
                        if extra > 0:
                            log_task_hours(task_id=t["id"], hours=extra)
                            st.rerun()
