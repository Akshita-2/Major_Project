import streamlit as st
from services.resume_generator import (
    create_enhanced_pdf_resume,
    create_word_resume,
    create_resume_package
)

def apply_hiredly_styles():
    """
    Applies custom CSS to the Streamlit app for the 'Hiredly' branding.
    This function is central to making the UI beautiful and modern.
    """
    custom_css = """
    <style>
        /* --- General App Styling --- */
        .stApp {
            background-color: #F0F4F8; /* Soft blue-grey background from config */
        }

        /* --- Custom Button Styles --- */
        .stButton>button {
            border-radius: 20px;
            border: 2px solid #1E90FF;
            color: #1E90FF;
            background-color: transparent;
            transition: all 0.3s ease-in-out;
            padding: 8px 20px;
            font-weight: bold;
        }
        .stButton>button:hover {
            border-color: #FFFFFF;
            color: #FFFFFF;
            background-color: #1E90FF;
        }
        /* Style for primary buttons */
        .stButton>button[kind="primary"] {
            background-color: #1E90FF;
            color: #FFFFFF;
        }
        .stButton>button[kind="primary"]:hover {
            background-color: #0073e6; /* A slightly darker blue on hover */
            border-color: #0073e6;
        }

        /* --- Header and Title Styling --- */
        h1, h2 {
            color: #2c3e50; /* A darker, more professional slate color */
        }
        
        /* --- Sidebar Styling --- */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF;
            border-right: 1px solid #e6e6e6;
        }

        /* --- Expander Styling --- */
        .stExpander {
            border: 1px solid #e6e6e6;
            border-radius: 10px;
        }
        
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)


def display_resume_preview(resume_data):
    """Shows a simplified, well-formatted preview of the resume content."""
    if not isinstance(resume_data, dict) or not resume_data:
        st.warning("No resume data available to display a preview.")
        return

    st.markdown(f"#### {resume_data.get('name', 'Your Name')}")
    st.write(f"📧 {resume_data.get('email', 'N/A')} | 📱 {resume_data.get('phone', 'N/A')}")
    
    with st.expander("🎯 Professional Summary", expanded=True):
        st.info(resume_data.get('summary', "No summary provided."))
    
    if resume_data.get('skills'):
        st.markdown("**💪 Core Skills**")
        # Display skills as neat tags
        skills_html = ''.join(f'<span style="background-color:#1E90FF;color:white;padding:5px 12px;border-radius:15px;margin:3px;display:inline-block;">{skill}</span>' for skill in resume_data['skills'])
        st.markdown(skills_html, unsafe_allow_html=True)
    
    if resume_data.get('experience'):
        st.markdown("**💼 Professional Experience**")
        for exp in resume_data['experience']:
            st.markdown(f"- {exp}")


def create_download_buttons(resume_data, selected_template):
    """Generates a column of download buttons for various resume formats."""
    st.subheader("Download Formats")
    
    # PDF Download
    with st.spinner("Generating PDF..."):
        pdf_buffer = create_enhanced_pdf_resume(resume_data, selected_template)
    st.download_button(
        label="📄 Download PDF",
        data=pdf_buffer,
        file_name=f"Hiredly_Resume_{resume_data.get('name', 'user').replace(' ', '_')}.pdf",
        mime="application/pdf",
        type="primary",
        use_container_width=True
    )
    
    # Word DOCX Download
    with st.spinner("Generating DOCX..."):
        word_buffer = create_word_resume(resume_data)
    st.download_button(
        label="📝 Download DOCX",
        data=word_buffer,
        file_name=f"Hiredly_Resume_{resume_data.get('name', 'user').replace(' ', '_')}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        use_container_width=True
    )
    
    # All-in-one ZIP Package
    with st.spinner("Generating ZIP Package..."):
        zip_buffer = create_resume_package(resume_data, selected_template)
    st.download_button(
        label="📦 Download Full Package (.zip)",
        data=zip_buffer,
        file_name="Hiredly_Resume_Package.zip",
        mime="application/zip",
        use_container_width=True
    )


def display_star_method_guide():
    """Displays a formatted guide for the STAR method."""
    st.subheader("⭐ Master the STAR Method for Behavioral Questions")
    star_cols = st.columns(4)
    with star_cols[0]:
        st.markdown("##### 🎯 Situation")
        st.write("Set the scene and provide context (when, where).")
    with star_cols[1]:
        st.markdown("##### 📋 Task")
        st.write("Describe your responsibility or the challenge.")
    with star_cols[2]:
        st.markdown("##### ⚡ Action")
        st.write("Explain the specific steps YOU took. Use 'I' statements.")
    with star_cols[3]:
        st.markdown("##### 🏆 Result")
        st.write("Share the outcome and quantify your success with numbers.")