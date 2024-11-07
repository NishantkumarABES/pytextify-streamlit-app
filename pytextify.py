import streamlit as st
from video_to_text import video_to_text
import time 

st.set_page_config(layout="wide")

st.image(r"images/logo_path.png", width=150)
st.title("Welcome to PyTextify")

st.subheader("Upload Files for Transcription")
uploaded_file = st.file_uploader(label = " ", type=["mp4"])
if uploaded_file is not None:
    file_name = uploaded_file.name
    with open("uploaded_file/uploaded_video.mp4", "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.video("uploaded_file/uploaded_video.mp4")  

    info_msg = st.info("Processing your video ...")
    transcription = video_to_text("uploaded_file/uploaded_video.mp4")
    info_msg.empty()
    st.success("Transcription is now available")
    def stream_data():
        for word in transcription.split(" "):
            yield word + " "
            time.sleep(0.02)   

    with st.container(border=True):
        st.write_stream(stream_data)
# Footer or additional info
st.write("---")
st.write("PyTextify © 2024. Transcribe your videos.")

ad_code = '''
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-7460908811855235"
     data-ad-slot="XXXXXXX"
     data-ad-format="auto">
</ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>
'''
st.markdown(ad_code, unsafe_allow_html=True)


# <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7460908811855235"
# crossorigin="anonymous"></script>