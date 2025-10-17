# pages/5_📥_Download_Resume.py

import streamlit as st
from services.ai_services import GeminiAIHelper
from components.ui_utils import display_resume_preview, create_download_buttons, apply_hiredly_styles
from components.sidebar import create_sidebar

def page_download_resume():
    """Defines the UI and logic for the final download page."""
    st.header("📥 Finalize and Download")
    st.markdown("Your resume has been optimized by Hiredly's AI. Choose a template and download your documents.")

    apply_hiredly_styles()

    # --- Authentication and Prerequisite Checks ---
    if not st.session_state.get('logged_in', False):
        st.warning("Please log in to access this feature.")
        st.stop()

    create_sidebar()

    if not st.session_state.get('resume_data'):
        st.info("Your downloadable resume will appear here.")
        st.warning("👈 Please provide your resume and a job description on the **Dashboard** and click 'Analyze & Prepare' first.")
        return

    resume_data = st.session_state.resume_data

    # --- Step 1: Template Selection ---
    st.subheader("🎨 Step 1: Choose Your Template")
    template_cols = st.columns(3)
    with template_cols[0]:
        if st.button("📋 Professional"):
            st.session_state.selected_template = "professional"
    with template_cols[1]:
        if st.button("🌟 Modern"):
            st.session_state.selected_template = "modern"
    with template_cols[2]:
        if st.button("🎨 Creative"):
            st.session_state.selected_template = "creative"
    
    selected_template = st.session_state.get('selected_template', 'professional')
    st.success(f"Selected Template: **{selected_template.title()}**")

    st.markdown("---")

    # The manual "AI Enhancements" section has been removed, as this is now automated on the Dashboard.

    # --- Step 2: Preview and Download ---
    st.subheader("👀 Step 2: Preview and Download")
    
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Live Preview of Your Optimized Resume")
        with st.container(border=True):
            display_resume_preview(resume_data)

    with col2:
        # This helper function now creates all the download buttons
        create_download_buttons(resume_data, selected_template)
        
    # --- Additional AI-Generated Content ---
    st.markdown("---")
    st.subheader("📄 Additional AI-Powered Documents")
    
    doc_col1, doc_col2 = st.columns(2)
    with doc_col1:
        if st.button("📝 Generate AI Cover Letter", use_container_width=True):
            if st.session_state.get('job_description'):
                with st.spinner("AI is writing your cover letter..."):
                    ai_helper = GeminiAIHelper(st.session_state.gemini_model)
                    st.session_state.cover_letter = ai_helper.generate_cover_letter(resume_data, st.session_state.job_description)
            else:
                st.warning("A job description is required to generate a targeted cover letter.")
    
    with doc_col2:
        if st.button("💼 Generate LinkedIn Summary", use_container_width=True):
            with st.spinner("AI is crafting your LinkedIn summary..."):
                ai_helper = GeminiAIHelper(st.session_state.gemini_model)
                st.session_state.linkedin_summary = ai_helper.generate_linkedin_summary(resume_data)

    # Display generated content if it exists
    if st.session_state.get('cover_letter'):
        st.text_area("Your AI-Generated Cover Letter:", st.session_state.cover_letter, height=250)
        st.download_button("📄 Download Cover Letter", st.session_state.cover_letter, "cover_letter.txt")

    if st.session_state.get('linkedin_summary'):
        st.text_area("Your AI-Generated LinkedIn Summary:", st.session_state.linkedin_summary, height=200)
        st.download_button("💼 Download LinkedIn Summary", st.session_state.linkedin_summary, "linkedin_summary.txt")

# --- Run the page ---
if __name__ == "__main__":
    page_download_resume()