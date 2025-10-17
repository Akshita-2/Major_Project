# pages/2_📊_ATS_Analysis.py

import streamlit as st
from components.visualizations import display_ats_gauge, display_keyword_wordcloud
from components.sidebar import create_sidebar
from components.ui_utils import apply_hiredly_styles

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
    """Defines the UI and logic for the ATS Analysis results page."""
    st.header("📊 ATS Analysis Report")
    st.markdown("Here is the detailed breakdown of your resume's compatibility with the job description.")
    
    apply_hiredly_styles()

    # --- Authentication and Sidebar ---
    if not st.session_state.get('logged_in', False):
        st.warning("Please log in from the main page to access Hiredly's tools.")
        st.stop()

    create_sidebar()
    
    # --- Display Pre-Computed Results ---
    st.markdown("---")
    
    # Check if the analysis results exist in the session state
    if 'ats_analysis_results' in st.session_state and isinstance(st.session_state.ats_analysis_results, dict):
        results = st.session_state.ats_analysis_results
        display_analysis_results(results)
    else:
        # Guide the user back to the dashboard if no results are found
        st.info("Your ATS analysis results will appear here.")
        st.warning("👈 Please provide your resume and a job description on the **Dashboard** page and click 'Analyze & Prepare' first.")

# --- Run the page ---
if __name__ == "__main__":
    page_ats_analysis()