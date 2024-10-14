import streamlit as st


with st.expander("Question and Answer"):
    question = st.text_input("Ask a question about the video content:")
    if st.button("Get Answer for YouTube"):
        # Assuming there's a function that fetches answers based on the query
        answer = "This is a sample answer for YouTube video."
        st.write(answer)