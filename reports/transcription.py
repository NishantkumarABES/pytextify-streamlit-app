import streamlit as st
import time

try: transcription = open("assets/transcription/text.txt", "r", encoding='utf-8').read()
except: transcription = None

def stream_data():
    for word in show_text.split(" "):
        yield word + " "
        time.sleep(0.02)

st.header("Avaliable Transcription")
if transcription:
    show_text = transcription[:1000]+" ..."
    with st.container(border=True):
        st.write_stream(stream_data)
    st.download_button(
        label= "Download full transcription",
        data = transcription,
        file_name = "English_Transcription.txt",
        mime="text/plain"
    )
else:
    st.error("No Transcription is avaliable.")