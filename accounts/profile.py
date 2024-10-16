import json
import streamlit as st
from utility_functions import is_valid_email

with open(r"assets\user_info.json", 'r') as json_file:
    user_data = json.load(json_file)


@st.dialog("Change User Information")
def edit_profile_info(name):
    st.write(f"Username: {name} ")
    new_name = st.text_input("New Name")
    if new_name: user_data["name"] = new_name
    new_email = st.text_input("New Email")
    if new_email: user_data["email"] = new_email
    st.write("---")
    password = st.text_input("Verify Password", type='password')
    if st.button("Submit"):
        if is_valid_email(new_email):
            if password == user_data["password"]:
                st.rerun()
            else: st.error("Incorrect Password")
        else: st.error("Invalid Email")


st.title("User Profile")
st.write("---")
st.subheader(user_data["name"])
st.write(f"**Username**: {user_data['username']}")
st.write(f"**Email**: {user_data['email']}")
if st.button("Edit Profile Details"): edit_profile_info(user_data["username"])

st.write("---")
st.write("PyTextify © 2024. Transcribe and summarize videos, documents, and more.")
