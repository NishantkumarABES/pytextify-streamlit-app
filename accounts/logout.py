import streamlit as st
from cookies_file import cookies


def logout():
    if "session_id" in cookies:
        session_id = cookies.get("session_id")
        if session_id in st.session_state.active_sessions:
            del st.session_state.active_sessions[session_id]
        cookies.delete("session_id")
    st.session_state.logged_in = False
    cookies.save()
    st.rerun()

if st.button("Log out"):
    logout()