import streamlit as st
from services.resume_generator import (
    create_enhanced_pdf_resume,
    create_word_resume,
    create_resume_package
)

def display_resume_preview(resume_data):
    """
    Shows a simplified, formatted preview of the resume content within the app.
    
    Args:
        resume_data (dict): The resume data to be displayed.
    """
    st.markdown(f"#### {resume_data.get('name', 'Your Name')}")
    st.write(f"📧 {resume_data.get('email', 'N/A')} | 📱 {resume_data.get('phone', 'N/A')}")
    
    if resume_data.get('summary'):
        st.markdown("**🎯 Professional Summary**")
        st.info(resume_data['summary'])
    
    if resume_data.get('skills'):
        st.markdown("**💪 Core Skills**")
        # Display skills in columns for better layout
        skills = resume_data['skills']
        cols = st.columns(3)
        for i, skill in enumerate(skills):
            with cols[i % 3]:
                st.markdown(f"- {skill}")

def display_star_method_guide():
    """Displays a formatted, four-column guide for the STAR method."""
    st.subheader("⭐ Master the STAR Method for Behavioral Questions")
    star_cols = st.columns(4)
    with star_cols[0]:
        st.markdown("**🎯 S - Situation**")
        st.write("Set the scene and provide context (when, where).")
    with star_cols[1]:
        st.markdown("**📋 T - Task**")
        st.write("Describe your goal or what was required of you.")
    with star_cols[2]:
        st.markdown("**⚡ A - Action**")
        st.write("Explain the specific steps *you* took to address the situation.")
    with star_cols[3]:
        st.markdown("**🏆 R - Result**")
        st.write("Share the outcome and quantify it whenever possible.")

def create_download_buttons(resume_data, selected_template):
    """
    Renders the download buttons for various resume formats.

    Args:
        resume_data (dict): The user's resume data.
        selected_template (str): The name of the visual template to apply.
    """
    st.subheader("Download Formats")
    
    # PDF Download
    try:
        pdf_buffer = create_enhanced_pdf_resume(resume_data, selected_template)
        st.download_button(
            label="📄 Download PDF",
            data=pdf_buffer,
            file_name=f"Resume_{resume_data.get('name', 'user').replace(' ', '_')}.pdf",
            mime="application/pdf",
            type="primary",
            use_container_width=True
        )
    except Exception as e:
        st.error(f"Failed to generate PDF: {e}")
        
    # Word DOCX Download
    try:
        word_buffer = create_word_resume(resume_data)
        st.download_button(
            label="📝 Download DOCX",
            data=word_buffer,
            file_name=f"Resume_{resume_data.get('name', 'user').replace(' ', '_')}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )
    except Exception as e:
        st.error(f"Failed to generate DOCX: {e}")

    # All-in-one ZIP Package
    try:
        zip_buffer = create_resume_package(resume_data, selected_template)
        st.download_button(
            label="📦 Download Full Package (.zip)",
            data=zip_buffer,
            file_name="AI_Resume_Package.zip",
            mime="application/zip",
            use_container_width=True
        )
    except Exception as e:
        st.error(f"Failed to generate ZIP package: {e}")