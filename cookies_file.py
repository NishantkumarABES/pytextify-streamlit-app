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

# Initialize cookies
cookies = EncryptedCookieManager(
    prefix="pytextify_",
    password=st.secrets["cookies_password"],
)
if not cookies.ready():
    st.stop()

# Generate unique session ID
def generate_session_id():
    return str(uuid.uuid4())

# Initialize session
def init_session():
    if "active_sessions" not in st.session_state:
        st.session_state["active_sessions"] = {}
