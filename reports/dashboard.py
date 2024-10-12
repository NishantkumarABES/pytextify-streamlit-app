import streamlit as st
from video_to_text import video_to_text
from utility_functions import extract_transcript_from_youtube

st.image(r"assets/images/logo_path.png", width=150)
st.title("Welcome to PyTextify")
# st.subheader("Transforming Media into Meaning – Fast, Accurate, Insightful!")

# Tabs for file upload or YouTube link input
tab1, tab2 = st.tabs(["Upload Files", "YouTube Link"])

# Tab 1: File Upload
with tab1:
    st.subheader("Upload Files for Transcription & Summarization")
    # File uploader for video, PDF, DOCX, or image
    uploaded_file = st.file_uploader("Choose a video, PDF, DOCX, or image", type=["mp4", "pdf", "docx", "jpg", "png"])

    if uploaded_file is not None:
        # Save the uploaded file locally
        with open("assets/uploaded_file/uploaded_video.mp4", "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Display the video
        st.video("assets/uploaded_file/uploaded_video.mp4")  
        st.write("Processing your file...")

        # Optional text area for video details or description
        video_description = st.text_area("Provide additional details or description for the uploaded video (optional)")

        if video_description:
            st.write("Video Description: ", video_description)

        # Process the video and generate a summary
        summary = video_to_text("assets/uploaded_file/uploaded_video.mp4") # Function to convert video to text and summarize
        def stream_data():
            for word in summary.split(" "):
                yield word + " "
                time.sleep(0.02)
        st.write_stream(stream_data)
        #st.success(summary)

        # Show Q&A panel after file upload
        with st.expander("Question and Answer"):
            question = st.text_input("Ask a question about the content:")
            if st.button("Get Answer"):
                # Assuming there's a function that fetches answers based on the query
                answer = "This is a sample answer."
                st.write(answer)

# Tab 2: YouTube Link
with tab2:
    st.subheader("Enter YouTube Video URL for Transcription & Summarization")
    youtube_url = st.text_input("YouTube Video URL")

    if youtube_url:
        # YouTube URL processing logic (dummy for now)
        st.write("Processing the YouTube video...")
        try: 
            summary = extract_transcript_from_youtube(youtube_url)
            st.success(summary)
        except:
            st.error("Oops! Our service is taking a quick break. Please try again later! 😥")
        
        # Show Q&A panel after processing YouTube video
        with st.expander("Question and Answer"):
            question = st.text_input("Ask a question about the video content:")
            if st.button("Get Answer for YouTube"):
                # Assuming there's a function that fetches answers based on the query
                answer = "This is a sample answer for YouTube video."
                st.write(answer)

# Footer or additional info
st.write("---")
st.write("PyTextify © 2024. Transcribe and summarize videos, documents, and more.")
