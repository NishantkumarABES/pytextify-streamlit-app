from streamlit_cookies_manager import EncryptedCookieManager
import streamlit as st


cookies = EncryptedCookieManager(
    prefix="pytextify_",  # Prefix for cookie name
    password="cookies_5430997924_py.secure-x-123",  # A secret password
)

if not cookies.ready():
    st.stop()
