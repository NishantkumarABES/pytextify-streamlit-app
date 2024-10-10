import sqlite3
import bcrypt
import streamlit as st
from cookies_file import cookies



# Database setup
conn = sqlite3.connect('pytextify_users.db', check_same_thread=False)
c = conn.cursor()

# Create a table to store users if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                name TEXT,
                password TEXT
            )''')
conn.commit()

def add_user(username, name, password):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    c.execute('INSERT INTO users (username, name, password) VALUES (?, ?, ?)', (username, name, hashed_password))
    conn.commit()

def check_user(username):
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    return c.fetchone()

def authenticate_user(username, password):
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    if user:
        return bcrypt.checkpw(password.encode(), user[3])
    return False

# Check cookies for existing login session


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
            username = st.text_input("Username", key='3')
            password = st.text_input("Password", type='password', key='4')
            
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
            new_user = st.text_input("Username", key='1')
            name = st.text_input("Name")
            col_left, col_right = st.columns([1, 1])
            with col_left:
                new_password = st.text_input("Password", type='password', key='2')
            with col_right:
                confirm_password = st.text_input("Confirm Password", type='password')
            if st.button("Sign Up"):
                if new_password == confirm_password:
                    if check_user(new_user) is None:
                        add_user(new_user, name, new_password)
                        st.success("You have successfully created an account!")
                        st.info("Go to the Login Menu to login")
                    else:
                        st.error("Username already exists! Try a different one.")
                else:
                    st.error("Passwords do not match")
        
        conn.close()



