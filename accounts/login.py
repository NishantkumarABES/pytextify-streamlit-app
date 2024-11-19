import bcrypt
import json
import streamlit as st
from cookies_file import cookies, generate_session_id
from utility_functions import is_valid_email
from TiDB_connection import session, user_table_query, insert_user_query, fetch_username_query
from sqlalchemy import text

user_info = dict()

# Creating user table
def create_user_table():
    with session.begin():
        session.execute(text(user_table_query))  # No need to close result explicitly
# create_user_table()

# Function to add a new user
def add_user(username, name, password, email):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    with session.begin():
        session.execute(
            text(insert_user_query),
            {"username": username, "name": name, "password": hashed_password, "email": email, "uploads": 0}
        )  

def check_user(username):
    with session.begin():
        result = session.execute(
            text(fetch_username_query),
            {"username": username}
        )
        row = result.first()  # Fetch the first row
    return row

# Authenticating a user
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
        user_data = {
            "username": user[1],
            "name": user[2],
            "email": user[4]
        }
        # Generate unique session ID
        session_id = generate_session_id()
        # Store in server-side session state
        st.session_state.active_sessions[session_id] = user_data
        # Store only session ID in cookie
        cookies["session_id"] = session_id
        cookies.save()
        return user_data
    return False




if not st.session_state.get("logged_in", False):
    # Streamlit app layout
    col1, col2 = st.columns([0.5, 4])
    with col1:
        st.image(r"assets/images/logo_path.png", width=100)
    with col2:
        st.title('PyTextify - Login & Sign Up')
    
    with st.container():
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        with tab1:
            st.subheader("Login to PyTextify")
            username = st.text_input("Username", key='1')
            password = st.text_input("Password", type='password', key='2')
            
            if st.button("Login"):
                if authenticate_user(username, password):
                    st.session_state.logged_in = True
                    user_info['password'] = password
                    json_obj = json.dumps(user_info, indent=4)
                    with open("assets/user_info.json", "w") as json_file:
                        json_file.write(json_obj)
                    cookies["logged_in"] = "true"  
                    cookies.save()
                    st.rerun()  
                else:
                    st.error("Incorrect username or password")
        with tab2:
            st.subheader("Create New Account")
            new_user = st.text_input("Username", key='3')
            

            col_left_1, col_right_1 = st.columns([1, 1])
            with col_left_1:
                name = st.text_input("Name", key='4')
            with col_right_1:
                email = st.text_input("E-mail" , key='5')
                


            col_left_2, col_right_2 = st.columns([1, 1])
            with col_left_2:
                new_password = st.text_input("Password", type='password', key='6')
            with col_right_2:
                confirm_password = st.text_input("Confirm Password", type='password', key='7')


            if st.button("Sign Up"):
                if new_password == confirm_password:
                    if not(email): st.error("Email field is empty.")
                    elif not(is_valid_email(email)): st.error("Invalid email format. Please enter a valid email address.")
                    elif not(name): st.error("Name field is empty.")
                    elif not(new_user                                                                                                                                                                                                       ): st.error("username field is empty.")
                    elif check_user(new_user) is None:
                        add_user(new_user, name, new_password, email)
                        st.success("You have successfully created an account!")
                        col_left_3, col_right_3 = st.columns([1, 1])
                        st.info("Go to the Login Menu to login.")
                    else:
                        st.error("Username already exists! Try a different one.")
                else:
                    st.error("Passwords do not match")
        




