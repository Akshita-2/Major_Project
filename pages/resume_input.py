# pages/1_🚀_Dashboard.py

import streamlit as st
from services.file_processors import (
    extract_text_from_pdf,
    extract_text_from_docx,
    process_video_resume
)
from services.ai_services import GeminiAIHelper
from components.ui_utils import apply_hiredly_styles, display_resume_preview
from agents import ResumeAgent
import speech_recognition as sr

def transcribe_audio_from_mic():
    """Listens for audio from the microphone and transcribes it."""
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            st.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            st.info("Listening... Speak now!")
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=60)
            st.info("Transcribing your answer...")
            text = recognizer.recognize_google(audio)
            st.toast("Transcription successful!", icon="✅")
            return text
    except sr.WaitTimeoutError:
        st.error("No speech detected. Please try again.")
    except sr.UnknownValueError:
        st.error("Could not understand the audio. Please speak clearly.")
    except sr.RequestError as e:
        st.error(f"API unavailable. Could not request results; {e}")
    except Exception as e:
        st.error(f"An error occurred with the microphone. Ensure PyAudio is installed and your mic has permission. Error: {e}")
    return ""

def page_dashboard():
    """Defines the UI and logic for the Hiredly Dashboard."""
    st.header("🚀 Hiredly Dashboard")
    st.markdown("This is your command center. Provide your resume and a job description to let the AI co-pilot prepare you for success.")
    
    # Apply the beautiful custom styles for Hiredly
    apply_hiredly_styles()

    if not st.session_state.get('logged_in', False):
        st.warning("Please log in from the main page to access the optimizer tools.")
        st.stop()

    ai_helper = GeminiAIHelper(st.session_state.gemini_model)
    resume_text_to_process = ""

    # --- Main Layout: Two columns for inputs ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Step 1: Provide Your Resume")
        input_tabs = st.tabs(["📝 Paste Text", "📎 Upload File", "🎤 Record Voice", "🎥 Upload Video"])
        
        with input_tabs[0]: # Paste Text
            resume_text_area = st.text_area("Paste your full resume text:", height=250)
        
        with input_tabs[1]: # Upload File
            uploaded_file = st.file_uploader("PDF or DOCX", type=['pdf', 'docx'])
        
        with input_tabs[2]: # Record Voice
            if st.button("🎤 Start Recording Your Summary"):
                transcribed_text = transcribe_audio_from_mic()
                st.session_state.voice_input = transcribed_text
            resume_text_to_process = st.text_area("Transcribed Text:", value=st.session_state.get('voice_input', ''), key="voice_text")
            
        with input_tabs[3]: # Upload Video
            video_file = st.file_uploader("MP4, MOV, AVI", type=['mp4', 'mov', 'avi'])

    with col2:
        st.subheader("Step 2: Add Target Job Description")
        job_desc = st.text_area("Paste the job description here:", height=300, key="job_desc_input")

    st.markdown("---")

    # --- The "Analyze Once" Button ---
    if st.button("🚀 Analyze & Prepare for Opportunity", type="primary", use_container_width=True):
        # Determine which input has content
        if resume_text_area:
            resume_text_to_process = resume_text_area
        elif uploaded_file:
            with st.spinner("Reading file..."):
                if uploaded_file.type == "application/pdf":
                    resume_text_to_process = extract_text_from_pdf(uploaded_file)
                else:
                    resume_text_to_process = extract_text_from_docx(uploaded_file)
        elif st.session_state.get('voice_input'):
            resume_text_to_process = st.session_state.voice_input
        elif video_file:
            with st.spinner("Extracting audio from video..."):
                resume_text_to_process = process_video_resume(video_file)
        
        # --- Validation and Full Analysis ---
        if not resume_text_to_process:
            st.error("Please provide your resume using one of the methods above.")
        elif not job_desc:
            st.error("Please paste the job description.")
        else:
            # This is the core of the new, fast workflow
            agent = ResumeAgent()
            with st.status("🚀 Engaging AI Co-Pilot...", expanded=True) as status:
                st.info(" Parsing and structuring your resume...")
                initial_data = ai_helper.analyze_resume_content(resume_text_to_process)
                st.session_state.resume_data = initial_data
                
                # Run the agent's full analysis to get everything at once
                all_results = agent.run_full_analysis(initial_data, job_desc)
                
                # Update session state with all the pre-computed results
                st.session_state.ats_analysis_results = all_results.get('ats')
                st.session_state.ats_score = all_results.get('ats', {}).get('ats_score', 0)
                st.session_state.interview_questions = all_results.get('questions')
                st.session_state.course_recommendations = all_results.get('courses')
                
                # Auto-apply the optimizations from the analysis
                optimization = all_results.get('optimization', {})
                if isinstance(optimization, dict):
                    st.info(" Applying automatic optimizations...")
                    st.session_state.resume_data['summary'] = optimization.get('optimized_summary', initial_data.get('summary', ''))
                    current_skills = set(st.session_state.resume_data.get('skills', []))
                    current_skills.update(optimization.get('missing_keywords', []))
                    st.session_state.resume_data['skills'] = sorted(list(current_skills))
                
                status.update(label="✅ Analysis Complete! You're ready to go.", state="complete")
            
            st.balloons()

    # --- Display Results Preview ---
    if 'resume_data' in st.session_state and st.session_state.resume_data:
        st.markdown("---")
        st.header("Your AI-Powered Analysis is Ready")
        display_resume_preview(st.session_state.resume_data)

# --- Run the page ---
if __name__ == "__main__":
    page_dashboard()