from streamlit_cookies_manager import EncryptedCookieManager
import streamlit as st


cookies = EncryptedCookieManager(
    prefix="pytextify_",  # Prefix for cookie name
    password= st.secrets["cookies_password"], # Password
)
if not cookies.ready():
    st.stop()
