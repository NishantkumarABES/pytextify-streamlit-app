import streamlit as st
from video_to_text import video_to_text
from utility_functions import extract_transcript_from_youtube
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

def english_to_hindi(text):
    hindi_text = transliterate(text, sanscript.ITRANS, sanscript.DEVANAGARI)
    return hindi_text

st.image(r"assets/images/logo_path.png", width=150)
st.title("Welcome to PyTextify")
# st.subheader("Transforming Media into Meaning – Fast, Accurate, Insightful!")

# Tabs for file upload or YouTube link input
tab1, tab2 = st.tabs(["Upload Files", "YouTube Link"])
transcription = None
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
        
        # Process the video and generate a summary
        
        language = st.radio(
            "Select the uploaded video language.",
            ['English', "Hindi"],
            index=None,
        )

        def save_file(transcription):
            video_description = st.text_area("Provide additional details or description for the uploaded video (optional)")
            if video_description:
                st.write("Video Description: ", video_description)
            transcription_file = open("assets/transcription/text.txt", "w", encoding='utf-8')
            transcription_file.write(transcription)
            st.success("Your Transtriction is now avaliable")

        if language == "Hindi":
            st.info("Processing your file...")
            transcription = video_to_text("assets/uploaded_file/uploaded_video.mp4") # Function to convert video to text and summarize
            transcription = english_to_hindi(transcription)
            save_file(transcription)
        elif language == "English": 
            st.info("Processing your file...")
            transcription = video_to_text("assets/uploaded_file/uploaded_video.mp4") # Function to convert video to text and summarize
            save_file(transcription)
        
        
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
        except Exception as E:
            st.write("Error message:", E)
            st.error("Oops! Our service is taking a quick break. Please try again later! 😥")
        
        

# Footer or additional info
st.write("---")
st.write("PyTextify © 2024. Transcribe and summarize videos, documents, and more.")
