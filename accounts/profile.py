import streamlit as st
from PIL import Image
import os

# Dummy user data
user_data = {
    "username": "john_doe",
    "name": "John Doe",
    "email": "john@example.com",
    "profile_pic": None,  # No profile picture initially
    "password": "test123"
}

@st.dialog("Change User Information")
def edit_profile_info(name):
    st.write(f"Username: {name} ")
    new_name = st.text_input("New Name")
    if new_name: user_data["name"] = new_name
    new_email = st.text_input("New Email")
    if new_email: user_data["email"] = new_email
    password = st.text_input("Password")
    if st.button("Submit"):
        if password == user_data["password"]:
            st.rerun()
        else: st.error("Incorrect Password")


st.title("User Profile")

# Profile picture section
col1, col2 = st.columns([1, 2])
with col1:
    if user_data["profile_pic"]:
        profile_pic = Image.open(user_data["profile_pic"])
        st.image(profile_pic, caption=user_data["username"], use_column_width=True)
    else:
        st.warning("No profile picture available. Please upload an image.")
        uploaded_image = st.file_uploader("Upload a profile picture", type=["jpg", "png", "jpeg"])

        if uploaded_image is not None:
            img_path = os.path.join("profile_pics", uploaded_image.name)
            with open(img_path, "wb") as f:
                f.write(uploaded_image.getbuffer())
            user_data["profile_pic"] = img_path
            st.image(img_path, caption="Uploaded Profile Picture", use_column_width=True)

# User details
with col2:
    st.subheader(user_data["name"])
    st.write(f"**Username**: {user_data['username']}")
    st.write(f"**Email**: {user_data['email']}")
    if st.button("Edit Profile Details"): edit_profile_info("Nishant Kumar")

st.write("---")

# Recent Activity (Optional)
st.subheader("Recent Activity")
st.write("Keep track of your latest file uploads, questions asked, and summaries.")
st.write("You have no recent activity at this time.")

