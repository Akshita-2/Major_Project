import streamlit as st
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def display_ats_gauge(score):
    """
    Renders a Plotly gauge chart to display the ATS score.

    Args:
        score (int or float): The ATS score to display (0-100).
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "ATS Compatibility Score", 'font': {'size': 20}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "#2E86C1"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 50], 'color': '#FADBD8'},
                {'range': [50, 80], 'color': '#FDEBD0'},
                {'range': [80, 100], 'color': '#D5F5E3'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 95
            }
        }
    ))
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)

def display_keyword_wordcloud(keywords):
    """
    Generates and displays a word cloud from a list of keywords.

    Args:
        keywords (list): A list of strings (keywords).
    """
    if not keywords:
        st.info("No missing keywords to display.")
        return

    # Join the keywords into a single string
    text = " ".join(keywords)

    try:
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='white',
            colormap='viridis',
            max_words=50,
            contour_width=3,
            contour_color='steelblue',
            collocations=False # Avoids grouping common word pairs
        ).generate(text)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Could not generate word cloud: {e}")

def display_skills_gap_chart(user_skills, required_skills):
    """
    Creates and displays a radar chart visualizing the skills gap.
    This is a simplified visualization for demonstration.

    Args:
        user_skills (list): A list of skills from the user's resume.
        required_skills (list): A list of skills from the job description.
    """
    user_skills_lower = {s.lower() for s in user_skills}
    # For demo, if required_skills is empty, use a default set.
    if not required_skills:
        required_skills = ['python', 'data analysis', 'machine learning', 'communication', 'project management', 'sql']
    required_skills_lower = {s.lower() for s in required_skills}
    
    # Combine all unique skills to form the axes of the radar chart
    labels = list(user_skills_lower.union(required_skills_lower))
    
    # Assign scores: 1 if the skill is present, 0.2 if missing (to create a visible shape)
    user_scores = [1 if skill in user_skills_lower else 0.2 for skill in labels]
    required_scores = [1 if skill in required_skills_lower else 0.2 for skill in labels]

    fig = go.Figure()

    # User's skills trace
    fig.add_trace(go.Scatterpolar(
        r=user_scores,
        theta=labels,
        fill='toself',
        name='Your Skills',
        line=dict(color='royalblue')
    ))
    
    # Required skills trace
    fig.add_trace(go.Scatterpolar(
        r=required_scores,
        theta=labels,
        fill='toself',
        name='Required Skills',
        line=dict(color='rgba(255, 100, 100, 0.8)') # A semi-transparent red
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=False, range=[0, 1.1])
        ),
        showlegend=True,
        title="Skills Gap Analysis"
    )

    st.plotly_chart(fig, use_container_width=True)