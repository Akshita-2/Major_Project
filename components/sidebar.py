import streamlit as st
from agents import ResumeAgent

def create_sidebar():
    """
    Renders the sidebar component for the Hiredly application.

    This new sidebar displays the latest analysis score and hosts the
    interactive AI Co-Pilot for ad-hoc tasks.
    """

    # --- Display Latest Analysis Score ---
    st.sidebar.markdown("---")
    st.sidebar.header("📊 Latest Analysis")

    if 'ats_score' in st.session_state and st.session_state.ats_score > 0:
        score = st.session_state.ats_score
        st.sidebar.metric("ATS Compatibility Score", f"{score:.1f}%")
        
        # Display the number of missing keywords if available
        if 'ats_analysis_results' in st.session_state:
            results = st.session_state.ats_analysis_results
            if isinstance(results, dict):
                missing_keywords_count = len(results.get('missing_critical_keywords', []))
                st.sidebar.metric("Keywords to Add", missing_keywords_count)
    else:
        st.sidebar.info("Your analysis results will appear here once you run a scan on the Dashboard.")

    # --- Interactive AI Co-Pilot ---
    st.sidebar.markdown("---")
    st.sidebar.header("🤖 AI Co-Pilot")

    # The assistant is only active if there's resume data to work with
    if not st.session_state.get('resume_data'):
        st.sidebar.warning("Please input your resume on the Dashboard to activate the Co-Pilot.")
    else:
        st.sidebar.success("Co-Pilot is ready! Ask for a specific task.")
        user_question = st.sidebar.text_input(
            "Ask the AI to help you:",
            placeholder="e.g., 'Rephrase my summary to be more impactful.'"
        )

        if st.sidebar.button("⚡ Ask Co-Pilot"):
            if user_question:
                agent = ResumeAgent()
                with st.sidebar.spinner("Co-Pilot is working..."):
                    # The agent's execute_task is designed for these ad-hoc requests
                    response = agent.execute_task(
                        task_description=user_question,
                        resume_data=st.session_state.resume_data,
                        job_description=st.session_state.get('job_description', '')
                    )

                    # The UI now intelligently handles the agent's response
                    if isinstance(response, dict) and 'error' not in response:
                        # If the agent returns optimization data, apply it directly
                        if 'optimized_summary' in response:
                            st.session_state.resume_data['summary'] = response['optimized_summary']
                        
                        if 'missing_keywords' in response:
                            current_skills = set(st.session_state.resume_data.get('skills', []))
                            current_skills.update(response['missing_keywords'])
                            st.session_state.resume_data['skills'] = sorted(list(current_skills))

                        st.sidebar.success("Your resume data has been updated!")
                        st.rerun() # Refresh the app to show changes instantly
                        
                    elif isinstance(response, dict) and 'error' in response:
                        st.sidebar.error(response['error'])
                    else:
                        # If the agent returns a simple string message, just display it
                        st.sidebar.info(response)
            else:
                st.sidebar.error("Please enter a task for the Co-Pilot.")