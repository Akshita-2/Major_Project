# pages/3_🎓_Course_Recommendations.py

import streamlit as st
import plotly.graph_objects as go
from components.sidebar import create_sidebar
from components.ui_utils import apply_hiredly_styles

def display_skills_gap_chart(user_skills, missing_skills):
    """
    Creates a dynamic radar chart visualizing the actual skills gap.
    """
    user_skills_lower = {s.lower() for s in user_skills}
    missing_skills_lower = {s.lower() for s in missing_skills}
    
    # The axes of our chart are the union of skills you have and skills you're missing.
    labels = sorted(list(user_skills_lower.union(missing_skills_lower)))
    
    # A required skill is one you have OR one that's missing.
    required_skills_lower = user_skills_lower.union(missing_skills_lower)

    # Assign scores: 1 if present, 0.2 if missing (to create a visible shape).
    user_scores = [1 if skill in user_skills_lower else 0.2 for skill in labels]
    required_scores = [1 if skill in required_skills_lower else 0.2 for skill in labels]

    fig = go.Figure()

    # Your Skills (Blue Area)
    fig.add_trace(go.Scatterpolar(
        r=user_scores, theta=labels, fill='toself', name='Your Skills',
        line=dict(color='#1E90FF')
    ))
    # Required Skills (Red Line Outline)
    fig.add_trace(go.Scatterpolar(
        r=required_scores, theta=labels, fill='none', name='Required Skills',
        line=dict(color='rgba(255, 100, 100, 0.8)')
    ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=False, range=[0, 1.1])),
        showlegend=True,
        title="Your Personalized Skills Gap",
        font=dict(color="#262730")
    )
    st.plotly_chart(fig, use_container_width=True)


def page_course_recommendations():
    """Defines the UI for the Course Recommendations results page."""
    st.header("🎓 AI-Powered Skill Development")
    st.markdown("Here are personalized recommendations to bridge your skill gaps and get you job-ready.")
    
    apply_hiredly_styles()

    if not st.session_state.get('logged_in', False):
        st.warning("Please log in to access Hiredly's tools.")
        st.stop()

    create_sidebar()
    st.markdown("---")

    # --- Display Pre-Computed Results ---
    if 'course_recommendations' in st.session_state and st.session_state.get('course_recommendations'):
        courses = st.session_state.course_recommendations
        ats_results = st.session_state.get('ats_analysis_results', {})
        resume_data = st.session_state.get('resume_data', {})
        missing_keywords = ats_results.get('missing_critical_keywords', [])
        
        col1, col2 = st.columns([3, 2])

        with col1:
            st.subheader("📈 Your Skills Gap Analysis")
            display_skills_gap_chart(resume_data.get('skills', []), missing_keywords)

        with col2:
            st.subheader("🎯 Priority Learning Areas")
            if missing_keywords:
                st.markdown("Based on your analysis, the AI recommends focusing on:")
                # Dynamically list the top missing keywords
                for i, keyword in enumerate(missing_keywords[:4]):
                    st.info(f"**Priority {i+1}:** {keyword.title()}")
            else:
                st.success("Excellent! No critical skill gaps were identified.")
        
        st.markdown("---")
        st.subheader("📚 Your Personalized Learning Plan")
        
        for i, course in enumerate(courses):
             if isinstance(course, dict):
                with st.expander(f"**{course.get('course_name', 'Unnamed Course')}** by {course.get('provider', 'N/A')}"):
                    st.markdown(f"**Why it's recommended:** {course.get('reason', 'N/A')}")
                    st.markdown(f"**Skill Gap Addressed:** `{course.get('skill_gap', 'General Skill')}`")
                    st.markdown(f"**Estimated Duration:** {course.get('duration', 'Variable')}")
                    st.button("🔗 View Course", key=f"course_btn_{i}") # Placeholder button

    else:
        # Guide the user back to the dashboard if no results are found
        st.info("Your personalized course recommendations will appear here.")
        st.warning("👈 Please provide your resume and a job description on the **Dashboard** and click 'Analyze & Prepare' first.")

if __name__ == "__main__":
    page_course_recommendations()