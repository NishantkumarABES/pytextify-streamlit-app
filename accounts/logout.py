import streamlit as st

if st.button("Log out"):
    st.session_state.logged_in = False
    st.rerun()