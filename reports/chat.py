import streamlit as st

# Initialize session state variables to store chat history
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Sidebar for user profile or additional options
# with st.sidebar:
#     st.header("Chat Options")
#     user_name = st.text_input("Your Name", placeholder="Enter your name...")
#     profile_pic = st.file_uploader("Upload Profile Picture", type=['jpg', 'png'])

#     if profile_pic:
#         st.image(profile_pic, caption="Your Profile Picture", use_column_width=True)

# Main chat interface
st.title("Chat with your uploaded file")

# Display chat history
if st.session_state['messages']:
    st.write("### Chat History")
    for message in st.session_state['messages']:
        if message['user'] == "user":
            st.write(f"**{message['name']}**: {message['content']}")
        else:
            st.write(f"**Bot**: {message['content']}")

# User input for chat
user_name = "Nishant Kumar"
with st.form(key='chat_form', clear_on_submit=True):
    user_input = st.text_input(f"Chat with {user_name if user_name else 'Bot'}", placeholder="Type your message here...")
    submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        # Add user message to chat history
        st.session_state['messages'].append({"user": "user", "name": user_name if user_name else "User", "content": user_input})

        # Simulate bot response (you can replace this with real logic)
        bot_response = f"I see you said: '{user_input}'"
        st.session_state['messages'].append({"user": "bot", "content": bot_response})

# Add a button to clear chat history
if st.button("Clear Chat"):
    st.session_state['messages'] = []   
    st.rerun()



# import streamlit as st


# with st.expander("Question and Answer"):
#     question = st.text_input("Ask a question about the video content:")
#     if st.button("Get Answer"):
#         # Assuming there's a function that fetches answers based on the query
#         answer = "This is a sample answer for YouTube video."
#         st.write(answer)