import regex as re
import bcrypt
import streamlit as st
from cookies_file import cookies
from TiDB_connection import engine, user_table_query, insert_user_query, fetch_username_query
from sqlalchemy import text

with engine.connect() as connection:
    connection.execute(text(user_table_query))


def add_user(username, name, password, email):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    with engine.connect() as connection:
        connection.execute(
            text(insert_user_query),
            {"username": username, "name": name, "password": hashed_password, "email": email}
        )
        
def check_user(username):
    with engine.connect() as connection:
        result = connection.execute(
            text(fetch_username_query),
            {"username": username}
        )
    return result.first()

def authenticate_user(username, password):
    with engine.connect() as connection:
        result = connection.execute(
            text(fetch_username_query),
            {"username": username}
        )
    user = result.first()
    if user:
        return bcrypt.checkpw(password.encode(), user[3].encode('utf-8'))
    return False

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email)



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
                        st.info("Go to the Login Menu to login.")
                    else:
                        st.error("Username already exists! Try a different one.")
                else:
                    st.error("Passwords do not match")
        




