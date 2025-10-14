import streamlit as st
import google.generativeai as genai

def initialize_session_state():
    """
    Initializes all necessary session state variables for the application.

    This function should be called once per session, typically after a user
    successfully logs in. It sets up the Gemini API connection and default
    values for the app's state.
    """
    # Use a flag to ensure this runs only once per session
    if 'initialized' in st.session_state:
        return

    # --- 1. CONFIGURE GEMINI API ---
    try:
        # Best practice: Use Streamlit secrets to store the API key
        # Create a file .streamlit/secrets.toml and add:
        # GEMINI_API_KEY = "YOUR_API_KEY"
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        
        # Store the initialized model in the session state for reuse
        st.session_state.gemini_model = genai.GenerativeModel('gemini-2.5-pro')
        st.toast("✅ Gemini AI Connected!", icon="🤖")

    except Exception as e:
        st.error("Could not configure Gemini AI. Please check your API key in Streamlit secrets.")
        st.error(f"Error: {e}")
        st.stop() # Stop the app if the AI model fails to load

    # --- 2. INITIALIZE APP STATE VARIABLES ---
    # These variables will hold data as the user navigates through the pages.
    
    # Data structures
    st.session_state.resume_data = {}
    st.session_state.job_description = ""
    st.session_state.ats_analysis_results = None
    st.session_state.course_recommendations = []
    st.session_state.interview_questions = []

    # UI and control states
    st.session_state.ats_score = 0
    st.session_state.selected_template = "professional"
    st.session_state.cover_letter = ""
    st.session_state.linkedin_summary = ""
    st.session_state.current_mock_question = None
    st.session_state.last_feedback = ""

    # Set the flag to indicate that initialization is complete
    st.session_state.initialized = True