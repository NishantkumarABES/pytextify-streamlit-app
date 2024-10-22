import streamlit as st
from llm_modal import generate_documnet
import time

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

st.title("Chat with your uploaded file")



with st.form(key='chat_form', clear_on_submit=True):
    user_input = st.text_input(label="**Write your query here**", placeholder="Type your message here...")
    submit_button = st.form_submit_button(label='Send')
    if submit_button:
        if user_input:
            response = generate_documnet(user_input, 'chat').text
            if response:
                def stream_data():
                    for word in response.split(" "):
                        yield word + " "
                        time.sleep(0.02)
                st.write_stream(stream_data)
            else: st.error("No file is uploaded yet.")
        else: st.error("Input feild is empty.")

# Add a button to clear chat history
if st.button("Clear Chat"):
    st.rerun()

