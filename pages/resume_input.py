import streamlit as st
from services.file_processors import (
    extract_text_from_pdf,
    extract_text_from_docx,
    process_voice_input,
    process_video_resume
)
from services.ai_services import GeminiAIHelper

def display_extracted_data(resume_data):
    """Displays a preview of the data extracted by the AI."""
    st.subheader("🤖 AI Analysis Complete")
    st.success("Resume data has been successfully extracted and analyzed!")

    col1, col2 = st.columns(2)
    with col1:
        st.write("**Name:**", resume_data.get('name', 'Not found'))
        st.write("**Email:**", resume_data.get('email', 'Not found'))
        st.write("**Phone:**", resume_data.get('phone', 'Not found'))

    with col2:
        st.write("**Top Skills Found:**")
        skills = resume_data.get('skills', [])
        if skills:
            for skill in skills[:5]:  # Show top 5 skills
                st.write(f"• {skill}")
        else:
            st.write("No skills found.")

    if resume_data.get('summary'):
        st.subheader("📄 AI-Generated Professional Summary")
        st.info(resume_data['summary'])

def page_resume_input():
    """Defines the UI and logic for the Resume Input page."""
    st.header("📄 Resume Input")
    st.markdown("Start here by providing your resume content. Our AI will analyze it to build your professional profile.")

    # --- Authentication Check ---
    if not st.session_state.get('logged_in', False):
        st.warning("Please log in from the main page to access the optimizer tools.")
        st.stop()

    # --- Initialize AI Helper ---
    ai_helper = GeminiAIHelper(st.session_state.gemini_model)

    # --- Input Method Selection ---
    input_method = st.selectbox(
        "Choose your input method:",
        ["📝 Text Input", "📎 File Upload", "🎤 Voice Input"],
        help="Select how you want to provide your resume."
    )

    st.markdown("---")

    # --- Logic for Text Input ---
    if input_method == "📝 Text Input":
        st.subheader("Type or Paste Your Resume Content")
        resume_text = st.text_area(
            "Paste your full resume text below:",
            height=300,
            placeholder="e.g., John Doe\nNew York, NY | (123) 456-7890 | john.doe@email.com..."
        )
        if st.button("🤖 Analyze Text with AI", type="primary"):
            if resume_text:
                with st.spinner("🧠 Gemini is analyzing your resume..."):
                    resume_data = ai_helper.analyze_resume_content(resume_text)
                    st.session_state.resume_data = resume_data
                display_extracted_data(resume_data)
            else:
                st.warning("Please paste your resume content before analyzing.")

    # --- Logic for File Upload ---
    elif input_method == "📎 File Upload":
        st.subheader("Upload Your Resume File")
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['pdf', 'docx', 'txt'],
            help="Supported formats: PDF, DOCX, TXT"
        )
        if st.button("🤖 Analyze File with AI", type="primary"):
            if uploaded_file:
                with st.spinner("Reading file and analyzing with Gemini..."):
                    resume_text = ""
                    if uploaded_file.type == "application/pdf":
                        resume_text = extract_text_from_pdf(uploaded_file)
                    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                        resume_text = extract_text_from_docx(uploaded_file)
                    else:
                        resume_text = uploaded_file.read().decode("utf-8")
                    
                    if resume_text:
                        resume_data = ai_helper.analyze_resume_content(resume_text)
                        st.session_state.resume_data = resume_data
                        display_extracted_data(resume_data)
                    else:
                        st.error("Could not extract text from the file. It might be empty or corrupted.")
            else:
                st.warning("Please upload a file first.")

    # --- Logic for Voice Input ---
    elif input_method == "🎤 Voice Input":
        st.subheader("Upload a Voice Recording of Your Resume")
        st.info("Record yourself summarizing your career and qualifications, then upload the audio file.")
        audio_file = st.file_uploader(
            "Upload an audio file",
            type=['wav', 'mp3', 'm4a'],
            help="Supported formats: WAV, MP3, M4A"
        )
        if st.button("🤖 Transcribe and Analyze Audio", type="primary"):
            if audio_file:
                with st.spinner("Transcribing audio and analyzing with Gemini..."):
                    resume_text = process_voice_input(audio_file)
                    if resume_text:
                        st.subheader("🎤 Transcribed Text:")
                        st.text_area("", value=resume_text, height=150, disabled=True)
                        resume_data = ai_helper.analyze_resume_content(resume_text)
                        st.session_state.resume_data = resume_data
                        display_extracted_data(resume_data)
                    else:
                        st.error("Could not transcribe the audio. Please try a clearer recording.")
            else:
                st.warning("Please upload an audio file first.")

# --- Run the page ---
if __name__ == "__main__":
    # This check ensures the page can be run standalone for testing if needed
    # but it's primarily designed to be run via Streamlit's multi-page app feature.
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        page_resume_input()
    else:
        st.warning("Please run the application from `main.py`")