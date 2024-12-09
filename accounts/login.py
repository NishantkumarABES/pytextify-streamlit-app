import bcrypt
import json
import streamlit as st
from utility_functions import log_errors
from cookies_file import cookies, generate_session_id, init_session
from utility_functions import is_valid_email
from TiDB_connection import session, user_table_query, insert_user_query, fetch_username_query
from sqlalchemy import text



user_info = {}

# Function to create user table
def create_user_table():
    with session.begin():
        session.execute(text(user_table_query))

# Add a new user
@log_errors
def add_user(username, name, password, email):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    with session.begin():
        session.execute(
            text(insert_user_query),
            {"username": username, "name": name, "password": hashed_password, "email": email, "uploads": 0}
        )

# Check if user exists
@log_errors
def check_user(username):
    with session.begin():
        result = session.execute(
            text(fetch_username_query),
            {"username": username}
        )
        return result.first()

# Authenticate user
Login_attempt = False
@log_errors
def authenticate_user(username, password):
    with session.begin():
        result = session.execute(
            text(fetch_username_query),
            {"username": username}
        )
        user = result.first()
    
    if user and bcrypt.checkpw(password.encode(), user[3].encode('utf-8')):
        user_info["username"] = user[1]
        user_info["name"] = user[2]
        user_info["email"] = user[4]
        session_id = generate_session_id()
        st.session_state["active_sessions"][session_id] = user_info
        cookies["session_id"] = session_id
        return user_info
    return False

# Streamlit UI
if not st.session_state.get("logged_in", False):
    col1, col2 = st.columns([0.5, 4])
    with col1:
        st.image("assets/images/logo_path.png", width=100)
    with col2:
        st.title("PyTextify - Login & Sign Up")
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    with tab1:
        st.subheader("Login to PyTextify")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login"):
            if authenticate_user(username, password):
                st.session_state.logged_in = True
                user_info["password"] = password
                with open("assets/user_info.json", "w") as json_file:
                    json.dump(user_info, json_file, indent=4)
                cookies["logged_in"] = "true"
                Login_attempt = True
            else:
                st.error("Incorrect username or password")
    with tab2:
        st.subheader("Create New Account")
        new_user = st.text_input("Username", key="signup_username")
        name = st.text_input("Name", key="signup_name")
        email = st.text_input("E-mail", key="signup_email")
        new_password = st.text_input("Password", type="password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_password")
        
        if st.button("Sign Up"):
            if new_password == confirm_password:
                if not email:
                    st.error("Email field is empty.")
                elif not is_valid_email(email):
                    st.error("Invalid email format.")
                elif not name:
                    st.error("Name field is empty.")
                elif not new_user:
                    st.error("Username field is empty.")
                elif check_user(new_user) is None:
                    add_user(new_user, name, new_password, email)
                    st.success("Account created successfully!")
                    st.info("Go to the Login menu to log in.")
                else:
                    st.error("Username already exists!")
            else:
                st.error("Passwords do not match.")
cookies.save()
if Login_attempt: st.rerun()