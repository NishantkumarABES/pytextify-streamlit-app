import moviepy.editor as mp
import speech_recognition as sr
from pydub import AudioSegment
import os
import math
from concurrent.futures import ThreadPoolExecutor


# Function to convert video to audio
def video_to_audio(video_path, audio_path):
    video = mp.VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)


# Function to split audio into chunks based on time duration (e.g., 30 seconds per chunk)
def split_audio_by_duration(audio_path, chunk_duration_ms=30000):
    audio = AudioSegment.from_wav(audio_path)
    # Calculate the number of chunks
   
    chunk_path = "assets/chunks"
    total_duration_ms = len(audio)  # Total duration in milliseconds
    num_chunks = math.ceil(total_duration_ms / chunk_duration_ms)  # Number of chunks
    chunks = []

    # Split audio into chunks
    for i in range(num_chunks):
        start = i * chunk_duration_ms
        end = start + chunk_duration_ms
        chunk = audio[start:end]
        # Export the chunk as a .wav file
        chunk_name = chunk_path + "/" + f"chunk_{i}.wav"
        chunk.export(chunk_name, format="wav")
        chunks.append(chunk_name)

    return chunks


# Function to convert audio chunks to text using Google Speech Recognition
def audio_to_text(audio_chunk):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_chunk) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "[Unintelligible audio]"
    except sr.RequestError as e:
        return f"Google API error: {e}"


# Function to convert video to text (processing smaller chunks of audio in threads)
def video_to_text(video_path, chunk_duration_ms=30000):
    if not(os.path.exists("assets/chunks")): os.mkdir("assets/chunks")
    # Step 1: Convert video to audio
    audio_path = video_path[:-4] + ".wav"
    video_to_audio(video_path, audio_path)
    # Step 2: Split audio into chunks
    chunks = split_audio_by_duration(audio_path, chunk_duration_ms)
    # Step 3: Convert each chunk to text concurrently using threads
    full_text = ""
    print("Total Number of chunks: ", len(chunks))
    # Use ThreadPoolExecutor to process chunks in parallel
    with ThreadPoolExecutor() as executor:
        chunk_texts = list(executor.map(audio_to_text, chunks))
    full_text = " ".join(chunk_texts)

    chunk_path = "assets/chunks"
    for chunk_file in os.listdir(chunk_path):
        os.remove(chunk_path + "/" + chunk_file)
    os.remove(audio_path)

    return full_text.strip()


