import streamlit as st
from cookies_file import cookies



if st.button("Log out"):
    st.session_state.logged_in = False
    cookies["logged_in"] = "false"
    cookies.save()
    st.rerun()

