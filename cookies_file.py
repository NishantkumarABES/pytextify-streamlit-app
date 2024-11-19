# from streamlit_cookies_manager import EncryptedCookieManager
# import streamlit as st


# cookies = EncryptedCookieManager(
#     prefix="pytextify_",  # Prefix for cookie name
#     password= st.secrets["cookies_password"], # Password
# )
# if not cookies.ready():
#     st.stop()


from streamlit_cookies_manager import EncryptedCookieManager
import streamlit as st
import uuid

cookies = EncryptedCookieManager(
    prefix="pytextify_",
    password=st.secrets["cookies_password"],
)

def generate_session_id():
    return str(uuid.uuid4())

def init_session():
    if not cookies.ready():
        st.stop()
    
    if 'active_sessions' not in st.session_state:
        st.session_state.active_sessions = {}