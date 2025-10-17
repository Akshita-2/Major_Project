# pages/4_💼_Interview_Prep.py

import streamlit as st
import random
import re
import speech_recognition as sr
from services.ai_services import GeminiAIHelper
from components.ui_utils import display_star_method_guide, apply_hiredly_styles
from components.sidebar import create_sidebar

def display_structured_feedback(feedback):
    """Parses and displays the AI's feedback in a structured format."""
    st.subheader("📝 AI Feedback")
    score_match = re.search(r"Overall Score:.*?(\d+)/10", feedback, re.IGNORECASE)
    score = int(score_match.group(1)) if score_match else 0
    
    try:
        well_section = feedback.split("✅ What Went Well:")[1].split("🔧 Areas for Improvement:")[0]
        improve_section = feedback.split("🔧 Areas for Improvement:")[1].split("⭐ A Stronger Example Answer:")[0]
        example_section = feedback.split("⭐ A Stronger Example Answer:")[1]
    except IndexError:
        st.markdown(feedback)
        return

    st.metric("Feedback Score", f"{score}/10")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**✅ What Went Well**")
        st.success(well_section)
    with col2:
        st.markdown("**🔧 Areas for Improvement**")
        st.warning(improve_section)
    with st.expander("⭐ See a Stronger Example Answer"):
        st.info(example_section)

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
    except Exception as e:
        st.error(f"Could not transcribe. Ensure PyAudio is installed and your mic has permission. Error: {e}")
    return ""

def page_interview_prep():
    """Defines the UI and logic for the enhanced Interview Preparation page."""
    st.header("💼 AI-Powered Interview Preparation")
    st.markdown("Practice with your personalized questions and get instant feedback from your AI career coach.")

    apply_hiredly_styles()

    if not st.session_state.get('logged_in', False):
        st.warning("Please log in to access this feature.")
        st.stop()

    create_sidebar()
    st.markdown("---")
    
    # --- Display Pre-Computed Results ---
    questions = st.session_state.get('interview_questions', [])

    if not questions:
        st.info("Your personalized interview questions will appear here.")
        st.warning("👈 Please provide your resume and a job description on the **Dashboard** and click 'Analyze & Prepare' first.")
        return
        
    all_categories = sorted(list(set(q.get('category', 'General').title() for q in questions if isinstance(q, dict))))
    filter_category = st.selectbox("🎯 Focus on a specific category:", ["All"] + all_categories)
    
    filtered_questions = questions
    if filter_category != "All":
        filtered_questions = [q for q in questions if isinstance(q, dict) and q.get('category', 'General').title() == filter_category]

    tab1, tab2 = st.tabs(["❓ Question Bank", "🎭 Mock Interview Simulator"])

    with tab1:
        st.subheader(f"Your Personalized Question Bank ({filter_category})")
        for q in filtered_questions:
            if isinstance(q, dict):
                with st.expander(q.get('question', 'N/A')):
                    st.info(f"**💡 Tip:** {q.get('tips', 'N/A')}")

    with tab2:
        st.subheader("AI Mock Interview Simulator")
        if not filtered_questions:
            st.warning(f"No questions found for '{filter_category}'. Please select another.")
            return

        if 'current_mock_question' not in st.session_state or st.session_state.current_mock_question not in filtered_questions:
            st.session_state.current_mock_question = random.choice(filtered_questions)
        
        q = st.session_state.current_mock_question

        if q and isinstance(q, dict):
            st.markdown(f"#### **AI Interviewer:**")
            st.info(f"*{q.get('question', '')}*")
            
            input_method = st.radio("Choose your answer method:", ["📝 Text", "🎤 Voice"], horizontal=True)
            
            if 'user_answer' not in st.session_state: st.session_state.user_answer = ""
            
            if input_method == "🎤 Voice":
                if st.button("🎤 Start Recording"):
                    transcribed_text = transcribe_audio_from_mic()
                    if transcribed_text: st.session_state.user_answer = transcribed_text
            
            st.session_state.user_answer = st.text_area("Your Answer:", value=st.session_state.user_answer, height=150, key="mock_answer_text")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("➡️ Get New Question"):
                    st.session_state.current_mock_question = random.choice(filtered_questions)
                    st.session_state.last_feedback = ""
                    st.session_state.user_answer = ""
                    st.rerun()
            with col2:
                if st.button("🤖 Get AI Feedback", type="primary"):
                    if st.session_state.user_answer:
                        with st.spinner("🤖 Evaluating your answer..."):
                            ai_helper = GeminiAIHelper(st.session_state.gemini_model)
                            feedback = ai_helper.evaluate_interview_answer(q.get('question'), st.session_state.user_answer, st.session_state.get('job_description', ''))
                            st.session_state.last_feedback = feedback
                    else:
                        st.warning("Please provide an answer to get feedback.")
            
            if st.session_state.get('last_feedback'):
                st.markdown("---")
                display_structured_feedback(st.session_state.last_feedback)
        else:
            st.error("Could not load a mock interview question. Please try generating questions again.")

    st.markdown("---")
    display_star_method_guide()

if __name__ == "__main__":
    page_interview_prep()