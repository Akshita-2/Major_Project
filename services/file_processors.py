import streamlit as st
import PyPDF2
import docx
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
import os

def extract_text_from_pdf(pdf_file):
    """
    Extracts text from an uploaded PDF file.

    Args:
        pdf_file: A file-like object from st.file_uploader.

    Returns:
        A string containing the extracted text, or an empty string on failure.
    """
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except Exception as e:
        st.error(f"Error reading PDF file: {e}")
        return ""

def extract_text_from_docx(docx_file):
    """
    Extracts text from an uploaded DOCX file.

    Args:
        docx_file: A file-like object from st.file_uploader.

    Returns:
        A string containing the extracted text, or an empty string on failure.
    """
    try:
        doc = docx.Document(docx_file)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    except Exception as e:
        st.error(f"Error reading DOCX file: {e}")
        return ""

def process_voice_input(audio_file):
    """

    Processes an uploaded audio file, converts it to text using speech recognition.
    Handles various audio formats by converting them to WAV first.
    Args:
        audio_file: A file-like object from st.file_uploader.
    Returns:
        A string containing the transcribed text, or an empty string on failure.
    """
    try:
        # pydub reads the audio file and its format
        sound = AudioSegment.from_file(audio_file)
        
        # Create a temporary file to store the WAV version
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
            sound.export(tmp_wav.name, format="wav")
            wav_path = tmp_wav.name

        # Use the speech_recognition library to process the WAV file
        r = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data)
        
        # Clean up the temporary file
        os.remove(wav_path)
        
        return text
    except sr.UnknownValueError:
        st.error("AI could not understand the audio. Please try a clearer recording.")
        return ""
    except sr.RequestError as e:
        st.error(f"Could not request results from the speech recognition service; {e}")
        return ""
    except Exception as e:
        st.error(f"Error processing audio file: {e}")
        return ""

def process_video_resume(video_file):
    """
    Placeholder function for processing a video resume.
    
    A full implementation would require libraries like moviepy to extract
    the audio track and then process it using the process_voice_input function.

    Args:
        video_file: A file-like object from st.file_uploader.

    Returns:
        A sample string, as this is a demo feature.
    """
    st.info("Video processing is a demo feature. A full implementation would extract and analyze the audio.")
    
    # In a real implementation, you would use a library like moviepy:
    # from moviepy.editor import VideoFileClip
    # with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_vid:
    #     tmp_vid.write(video_file.read())
    #     video = VideoFileClip(tmp_vid.name)
    #     audio = video.audio
    #     # Then save and process the audio file
    #     ...
    
    # For now, we return sample text.
    return "This is sample text from a video resume. The candidate has five years of experience in software development and is skilled in Python, React, and AWS."