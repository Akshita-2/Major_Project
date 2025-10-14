import streamlit as st
from agents.resume_agent import ResumeAgent

def create_sidebar():
    """
    Renders the sidebar component for the application.

    This function creates the job description text area and the AI agent 
    interaction section, managing their state through Streamlit's session state.
    """

    # --- Job Description Input ---
    st.sidebar.markdown("---")
    st.sidebar.header("🎯 Job Description")
    st.sidebar.info("Paste the job description for the role you're targeting. The AI will use this for all analyses.")

    # The text_area's value is tied to the session state to persist across pages
    job_desc = st.sidebar.text_area(
        "Paste the job description here:",
        value=st.session_state.get('job_description', ''),
        height=250,
        key="job_desc_input" # A unique key is good practice
    )
    
    # Update the session state whenever the text_area changes
    st.session_state.job_description = job_desc

    # --- AI Agent Assistant ---
    st.sidebar.markdown("---")
    st.sidebar.header("🤖 AI Assistant")
    
    # Display a warning if prerequisites are not met
    if not st.session_state.get('resume_data') or not st.session_state.get('job_description'):
        st.sidebar.warning("Please input your resume and a job description to activate the AI Assistant.")
    else:
        st.sidebar.success("AI Assistant is ready! Ask a question below.")
        user_question = st.sidebar.text_input(
            "Ask the AI to help you:",
            placeholder="e.g., 'Improve my summary'"
        )

        if st.sidebar.button("⚡ Ask AI Assistant"):
            if user_question:
                agent = ResumeAgent()
                with st.sidebar.spinner("Agent is on it..."):
                    response = agent.execute_task(
                        task_description=user_question,
                        resume_data=st.session_state.resume_data,
                        job_description=st.session_state.job_description
                    )
                    st.sidebar.info(f"**Agent Response:** {response}")
                    # Use st.rerun() if the agent's action should immediately refresh the main page content
                    st.rerun()
            else:
                st.sidebar.error("Please enter a question for the assistant.")