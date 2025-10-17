import streamlit as st
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def display_ats_gauge(score):
    """
    Renders a Plotly gauge chart styled for the Hiredly theme.
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "ATS Compatibility Score", 'font': {'size': 20, 'color': '#262730'}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "#1E90FF"},  # UPDATED: Hiredly primary color
            'bgcolor': "white",
            'borderwidth': 1,
            'bordercolor': "#e6e6e6",
            'steps': [
                {'range': [0, 50], 'color': '#FADBD8'},
                {'range': [50, 80], 'color': '#FDEBD0'},
                {'range': [80, 100], 'color': '#D5F5E3'}
            ],
        }
    ))
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20), font=dict(color="#262730"))
    st.plotly_chart(fig, use_container_width=True)

def display_keyword_wordcloud(keywords):
    """
    Generates and displays a word cloud from a list of keywords.
    """
    if not keywords:
        st.info("No missing keywords to display.")
        return

    text = " ".join(keywords)
    try:
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='white',
            colormap='Blues_r',  # UPDATED: Blue colormap to match theme
            max_words=50,
            collocations=False
        ).generate(text)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Could not generate word cloud: {e}")

def display_skills_gap_chart(user_skills, missing_skills):
    """
    Creates and displays a dynamic radar chart visualizing the actual skills gap.
    """
    user_skills_lower = {s.lower() for s in user_skills}
    missing_skills_lower = {s.lower() for s in missing_skills}
    
    # The axes of our chart are the union of skills you have and skills you're missing.
    labels = sorted(list(user_skills_lower.union(missing_skills_lower)))
    
    if not labels:
        st.info("Not enough skill data to generate a gap analysis chart.")
        return
        
    # A required skill is one you have OR one that's missing.
    required_skills_lower = user_skills_lower.union(missing_skills_lower)

    # Assign scores: 1 if present, 0.2 if missing (to create a visible shape).
    user_scores = [1 if skill in user_skills_lower else 0.2 for skill in labels]
    required_scores = [1 if skill in required_skills_lower else 0.2 for skill in labels]

    fig = go.Figure()

    # Required Skills (Red Area - the gap to fill)
    fig.add_trace(go.Scatterpolar(
        r=required_scores, theta=labels, fill='toself', name='Required Skills',
        fillcolor='rgba(231, 76, 60, 0.2)',
        line=dict(color='rgba(231, 76, 60, 0.8)')
    ))
    # Your Skills (Blue Area)
    fig.add_trace(go.Scatterpolar(
        r=user_scores, theta=labels, fill='toself', name='Your Skills',
        fillcolor='rgba(30, 144, 255, 0.4)',      # UPDATED: Hiredly primary color (semi-transparent)
        line=dict(color='#1E90FF')                # UPDATED: Hiredly primary color
    ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=False, range=[0, 1.1])),
        showlegend=True,
        title="Your Personalized Skills Gap",
        font=dict(color="#262730")
    )
    st.plotly_chart(fig, use_container_width=True)