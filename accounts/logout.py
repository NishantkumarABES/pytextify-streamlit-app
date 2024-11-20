import streamlit as st
from cookies_file import cookies

def logout():
    # Check if the session_id exists in cookies
    if "session_id" in cookies:
        session_id = cookies.get("session_id", "")
        if session_id in st.session_state.active_sessions:
            del st.session_state.active_sessions[session_id]
        # Invalidate the session_id by setting it to an empty string
        cookies["session_id"] = ""
    # Update session state to indicate logged-out status
    st.session_state.logged_in = False
    cookies.save()  # Save cookies after changes
    st.rerun()  # Refresh the app to apply changes

if st.button("Log out"):
    logout()
