import streamlit as st
st.set_page_config(layout="wide")

from cookies_file import cookies

login_page = st.Page("accounts/login.py", title="Pytextify - Log in & Sign up", icon=":material/login:")
logout_page = st.Page("accounts/logout.py", title="Log out", icon=":material/logout:")

dashboard = st.Page("reports/dashboard.py", title="Pytextify", icon=":material/dashboard:", default=True)
bugs = st.Page("reports/bugs.py", title="Bug reports", icon=":material/bug_report:")
alerts = st.Page("reports/alerts.py", title="System alerts", icon=":material/notification_important:")

search = st.Page("tools/search.py", title="Search", icon=":material/search:")
history = st.Page("tools/history.py", title="History", icon=":material/history:")


if cookies.get("logged_in") == "true":
    st.session_state.logged_in = True
else: st.session_state.logged_in = False

if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Account": [logout_page],
            "Reports": [dashboard, bugs, alerts],
            "Tools": [search, history],
        }
    )
else: pg = st.navigation([login_page])

pg.run()