import streamlit as st
from services.ai_services import GeminiAIHelper
from components.ui_utils import display_resume_preview, create_download_buttons
from components.sidebar import create_sidebar

def page_download_resume():
    """Defines the UI and logic for the final download page."""
    st.header("📥 Finalize and Download Your Resume")
    st.markdown("Select a template, apply final AI enhancements, and download your career-ready documents.")

    # --- Authentication and Prerequisite Checks ---
    if not st.session_state.get('logged_in', False):
        st.warning("Please log in from the main page to access this feature.")
        st.stop()

    create_sidebar()

    if not st.session_state.get('resume_data'):
        st.info("👈 Please start by inputting your resume on the 'Resume Input' page.")
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

    # --- Step 2: Final AI Enhancements ---
    st.subheader("🤖 Step 2: Apply Final AI Enhancements (Optional)")
    enhancement_options = st.multiselect(
        "Select enhancements to apply:",
        ["🎯 Optimize summary for job match", "🔍 Add missing keywords from job description"],
        help="The AI will refine your resume based on these selections. Requires a job description in the sidebar."
    )

    if st.button("🚀 Apply AI Enhancements", type="primary"):
        if enhancement_options and st.session_state.get('job_description'):
            with st.spinner("🤖 AI is applying the final touches..."):
                ai_helper = GeminiAIHelper(st.session_state.gemini_model)
                optimization = ai_helper.optimize_resume_for_job(resume_data, st.session_state.job_description)
                
                if isinstance(optimization, dict):
                    if "🎯 Optimize summary for job match" in enhancement_options:
                        st.session_state.resume_data['summary'] = optimization.get('optimized_summary', resume_data.get('summary', ''))
                    if "🔍 Add missing keywords from job description" in enhancement_options:
                        current_skills = set(st.session_state.resume_data.get('skills', []))
                        missing = optimization.get('missing_keywords', [])
                        current_skills.update(missing)
                        st.session_state.resume_data['skills'] = sorted(list(current_skills))
                    
                    st.success("Enhancements applied!")
                    st.rerun()
                else:
                    st.error("AI enhancement failed. Could not get a valid response.")
        else:
            st.warning("Please select at least one enhancement and ensure a job description is provided in the sidebar.")

    st.markdown("---")

    # --- Step 3: Preview and Download ---
    st.subheader("👀 Step 3: Preview and Download")
    
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Live Preview")
        with st.container(border=True):
            # Using the helper function for a clean preview
            display_resume_preview(resume_data)

    with col2:
        # Using the helper function to create all download buttons
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
                st.warning("Please add a job description in the sidebar first.")
    
    with doc_col2:
        if st.button("💼 Generate LinkedIn Summary", use_container_width=True):
            with st.spinner("AI is crafting your LinkedIn summary..."):
                ai_helper = GeminiAIHelper(st.session_state.gemini_model)
                st.session_state.linkedin_summary = ai_helper.generate_linkedin_summary(resume_data)

    # Display generated content if it exists in the session state
    if st.session_state.get('cover_letter'):
        st.text_area("**Your AI-Generated Cover Letter**", st.session_state.cover_letter, height=250)
        st.download_button("📄 Download Cover Letter", st.session_state.cover_letter, "cover_letter.txt")

    if st.session_state.get('linkedin_summary'):
        st.text_area("**Your AI-Generated LinkedIn Summary**", st.session_state.linkedin_summary, height=200)
        st.download_button("💼 Download LinkedIn Summary", st.session_state.linkedin_summary, "linkedin_summary.txt")

# --- Run the page ---
if __name__ == "__main__":
    page_download_resume()