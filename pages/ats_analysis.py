import streamlit as st
from services.ai_services import GeminiAIHelper
from components.visualizations import display_ats_gauge, display_keyword_wordcloud
from components.sidebar import create_sidebar
from database.db_manager import save_resume
# We no longer need the agent import here, as the action is now direct.

def display_analysis_results(results):
    """A helper function to display the formatted ATS analysis results."""
    st.subheader("📈 AI Analysis Breakdown")

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        display_ats_gauge(results.get('ats_score', 0))
    with col2:
        st.metric("Keyword Match", f"{results.get('keyword_match_percentage', 0):.1f}%")
        st.metric("Formatting Score", f"{results.get('formatting_score', 0):.1f}%")
    with col3:
        st.metric("Content Relevance", f"{results.get('content_relevance_score', 0):.1f}%")
        st.metric("Missing Keywords", len(results.get('missing_critical_keywords', [])))

    st.markdown("---")

    res_col1, res_col2 = st.columns(2)
    with res_col1:
        st.subheader("🎯 Strengths")
        for strength in results.get('strengths', ["No specific strengths identified."]):
            st.success(f"✅ {strength}")
        
        st.subheader("🔧 Improvement Areas")
        for improvement in results.get('improvement_areas', ["No specific improvements suggested."]):
            st.warning(f"⚠️ {improvement}")

    with res_col2:
        st.subheader("🔍 Missing Critical Keywords")
        missing_keywords = results.get('missing_critical_keywords', [])
        if missing_keywords:
            display_keyword_wordcloud(missing_keywords)
        else:
            st.info("Great job! No critical keywords seem to be missing.")

def page_ats_analysis():
    """Defines the UI and logic for the ATS Analysis page."""
    st.header("📊 ATS Compatibility Analysis & Auto-Optimization")
    st.markdown("Analyze your resume against a job description. The AI will then automatically optimize your content.")
    
    # --- Authentication and Prerequisite Checks ---
    if not st.session_state.get('logged_in', False):
        st.warning("Please log in from the main page to access the optimizer tools.")
        st.stop()

    create_sidebar()
    
    if not st.session_state.get('resume_data'):
        st.info("👈 Please start by providing your resume in the 'Resume Input' page.")
        return
    
    if not st.session_state.get('job_description'):
        st.info("👈 Please paste a job description into the sidebar to perform an analysis.")
        return

    st.markdown("---")

    # MODIFICATION 1: Changed the button text to reflect the new action.
    if st.button("🤖 Analyze and Auto-Optimize Resume", type="primary"):
        # MODIFICATION 2: Updated spinner text.
        with st.spinner("🔬 Step 1: Performing deep ATS analysis..."):
            ai_helper = GeminiAIHelper(st.session_state.gemini_model)
            resume_data = st.session_state.resume_data
            resume_text = " ".join(map(str, [
                resume_data.get('summary', ''),
                " ".join(map(str, resume_data.get('skills', []))),
                " ".join(map(str, resume_data.get('experience', []))),
                " ".join(map(str, resume_data.get('education', [])))
            ]))
            
            ats_analysis = ai_helper.score_resume_ats(resume_text, st.session_state.job_description)
            st.session_state.ats_analysis_results = ats_analysis

        if isinstance(ats_analysis, dict):
            new_score = ats_analysis.get('ats_score', 0)
            st.session_state.ats_score = new_score
            
            # MODIFICATION 3: Add the automatic optimization step.
            with st.spinner("✨ Step 2: Automatically optimizing your resume..."):
                optimization_results = ai_helper.optimize_resume_for_job(resume_data, st.session_state.job_description)

                # MODIFICATION 4: Apply the optimizations directly to the session state.
                if isinstance(optimization_results, dict):
                    # Update summary
                    optimized_summary = optimization_results.get('optimized_summary')
                    if optimized_summary:
                        st.session_state.resume_data['summary'] = optimized_summary

                    # Update skills
                    missing_keywords = optimization_results.get('missing_keywords', [])
                    if missing_keywords:
                        current_skills = set(st.session_state.resume_data.get('skills', []))
                        current_skills.update(missing_keywords)
                        st.session_state.resume_data['skills'] = sorted(list(current_skills))
                    
                    # MODIFICATION 5: Provide clear feedback to the user.
                    st.success("✅ **Automatic Optimization Complete!** Your resume's summary and skills have been updated in the session.")
                    st.balloons()

            # Save the analysis to history after all updates
            try:
                save_resume(st.session_state.user_id, st.session_state.resume_data, st.session_state.job_description, new_score)
                st.toast("Analysis and optimizations saved to your history!", icon="💾")
            except Exception as e:
                st.error(f"Could not save analysis to history. Error: {e}")
        else:
            st.error("AI analysis failed to return a valid format. Please try again.")

    # --- Display Analysis Results ---
    if 'ats_analysis_results' in st.session_state:
        results = st.session_state.ats_analysis_results
        if isinstance(results, dict) and results:
            display_analysis_results(results)
        else:
            st.warning("Analysis has not been run yet, or the last attempt failed. Click the button above.")
    
    # MODIFICATION 6: The manual agent section is no longer needed here and has been removed.

# --- Run the page ---
if __name__ == "__main__":
    page_ats_analysis()