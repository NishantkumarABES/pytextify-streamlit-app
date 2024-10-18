import json
import time
import docx
import streamlit as st
from video_to_text import video_to_text
from utility_functions import download_youtube_video
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
from TiDB_connection import session, update_uploads
from llm_modal import generate_documnet
from sqlalchemy import text
from pypdf import PdfReader



with open(r"assets\user_info.json", 'r') as json_file:
    user_data = json.load(json_file)


def english_to_hindi(text):
    hindi_text = transliterate(text, sanscript.ITRANS, sanscript.DEVANAGARI)
    return hindi_text

st.image(r"assets/images/logo_path.png", width=150)
st.title("Welcome to PyTextify")

tab1, tab2 = st.tabs(["Upload Files", "YouTube Link"])

if 'document' not in st.session_state:
    st.session_state.document = None

# Tab 1: File Upload
with tab1:
    st.subheader("Upload Files for Transcription & Summarization")
    uploaded_file = st.file_uploader("Choose a video, PDF, and DOCX", type=["mp4", "pdf", "docx"])
    if uploaded_file is not None:
        with session.begin():
            session.execute(text(update_uploads),{"username": user_data['username']})
            
        file_name = uploaded_file.name
        if file_name.endswith(".mp4"):
            with open("assets/uploaded_file/uploaded_video.mp4", "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.video("assets/uploaded_file/uploaded_video.mp4")  
            language = st.radio(
                "Select the uploaded video language.",
                ['English', "Hindi"],
                index=None,
            )

            def save_file(transcription):
                transcription_file = open("assets/transcription/text.txt", "w", encoding='utf-8')
                transcription_file.write(transcription)
                st.success("Your transcription is now available")

            def build_document(transcription):
                st.info("Generating your document.")
                document = generate_documnet(transcription, "video").text
                def stream_data():
                    for word in document.split(" "):
                        yield word + " "
                        time.sleep(0.02)
                with st.container(border=True):
                    st.write_stream(stream_data)
                st.session_state.document = document

            if language == "Hindi":
                st.info("Processing your file...")
                transcription = video_to_text("assets/uploaded_file/uploaded_video.mp4")  # Function to convert video to text and summarize
                transcription = english_to_hindi(transcription)
                save_file(transcription)
                build_document(transcription)

            elif language == "English": 
                st.info("Processing your file...")
                transcription = video_to_text("assets/uploaded_file/uploaded_video.mp4")  # Function to convert video to text and summarize
                save_file(transcription)
                build_document(transcription)
        
        if file_name.endswith('.docx'):
            with open("assets/uploaded_file/uploaded_file.docx", "wb") as f:
                f.write(uploaded_file.getbuffer())
            doc = docx.Document("assets/uploaded_file/uploaded_file.docx")
            full_text = []
            for paragraph in doc.paragraphs:
                full_text.append(paragraph.text)
    
            total_content =  '\n'.join(full_text)
            def build_document(content):
                st.info("Generating your document.")
                document = generate_documnet(content, None).text
                def stream_data():
                    for word in document.split(" "):
                        yield word + " "
                        time.sleep(0.02)
                with st.container(border=True):
                    st.write_stream(stream_data)
                st.session_state.document = document
            build_document(total_content)
        

        if file_name.endswith('.pdf'):
            with open("assets/uploaded_file/uploaded_file.pdf", "wb") as f:
                f.write(uploaded_file.getbuffer())

            reader = PdfReader("assets/uploaded_file/uploaded_file.pdf")
            total_content = ""
            for page in reader.pages:
                total_content += page.extract_text()
            
            def build_document(content):
                st.info("Generating your document.")
                document = generate_documnet(content, None).text
                def stream_data():
                    for word in document.split(" "):
                        yield word + " "
                        time.sleep(0.02)
                with st.container(border=True):
                    st.write_stream(stream_data)
                st.session_state.document = document
            build_document(total_content)
        
        


    if st.session_state.document and not(uploaded_file):
        with st.container(border=True):
            st.write(st.session_state.document)
        if st.button("Remove Document"):
            st.session_state.document = None
            st.rerun()

# Tab 2: YouTube Link
with tab2:
    st.subheader("Enter YouTube Video URL for Transcription & Summarization")
    youtube_url = st.text_input("YouTube Video URL")

    if youtube_url:
        st.write("Processing the YouTube video...")
        try: 
            video_title = download_youtube_video(youtube_url)
            st.write(video_title)
            st.video('assets/youtube_video/' + video_title)
        except Exception as E:
            st.error("Oops! Our service is taking a quick break. Please try again later! 😥")

# Footer or additional info
st.write("---")
st.write("PyTextify © 2024. Transcribe and summarize videos, documents, and more.")
