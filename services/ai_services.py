import streamlit as st
import json
import re
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from io import BytesIO

class GeminiAIHelper:
    """
    A service class to handle all interactions with the Google Gemini API.
    It abstracts the prompt engineering and API call logic away from the UI.
    """
    
    def __init__(self, model):
        """Initializes the helper with a configured Gemini model instance."""
        self.model = model

    def _safe_generate_content(self, prompt):
        """A wrapper for API calls to handle potential errors."""
        try:
            response = self.model.generate_content(prompt)
            # Accessing parts can sometimes be safer
            return response.text
        except Exception as e:
            st.error(f"An error occurred with the AI service: {e}")
            return None

    def _extract_json(self, text, start_char='{', end_char='}'):
        """
        Safely extracts a JSON object or array from a string.
        This is a robust fallback in case the model includes extra text.
        """
        if not text:
            return {} if start_char == '{' else []
            
        try:
            # Find the first '{' or '[' and the last '}' or ']'
            start_index = text.find(start_char)
            end_index = text.rfind(end_char)
            
            if start_index != -1 and end_index != -1 and end_index > start_index:
                json_str = text[start_index : end_index + 1]
                return json.loads(json_str)
            else:
                # Fallback for simple cases where the whole text might be the json
                return json.loads(text)
        except (json.JSONDecodeError, IndexError) as e:
            st.warning(f"Could not parse AI response into JSON. Error: {e}")
        
        return {} if start_char == '{' else []

    def analyze_resume_content(self, resume_text):
        """Uses Gemini to parse raw resume text into a structured JSON object."""
        prompt = f"""
        Analyze the following resume text and extract structured information.
        Your response MUST be a single, valid JSON object and nothing else.
        Do not include markdown backticks (```json), introductory text, or any other characters outside of the JSON structure.
        If a section is missing, provide an empty list or an empty string.

        Resume Text:
        ---
        {resume_text}
        ---

        Return a single JSON object with this exact structure:
        {{
            "name": "string", "email": "string", "phone": "string", "summary": "string",
            "skills": ["list", "of", "skills"],
            "experience": ["list of detailed work experience entries"],
            "education": ["list of education entries"],
            "certifications": ["list of certifications, if any"],
            "projects": ["list of projects, if any"]
        }}
        """
        response_text = self._safe_generate_content(prompt)
        return self._extract_json(response_text)

    def score_resume_ats(self, resume_text, job_description):
        """Provides a detailed ATS analysis and score as a JSON object."""
        prompt = f"""
        Act as an expert ATS (Applicant Tracking System). Analyze the resume against the job description.
        Your response MUST be a single, valid JSON object and nothing else.
        Do not add markdown formatting or any explanatory text.

        Resume: --- {resume_text} ---
        Job Description: --- {job_description} ---

        Return a single JSON object with this exact structure:
        {{
            "ats_score": number, "keyword_match_percentage": number,
            "missing_critical_keywords": ["list of important missing keywords"],
            "strengths": ["list of what the resume does well"],
            "improvement_areas": ["list of specific areas to improve"],
            "formatting_score": number, "content_relevance_score": number
        }}
        """
        response_text = self._safe_generate_content(prompt)
        return self._extract_json(response_text)

    def optimize_resume_for_job(self, resume_data, job_description):
        """Generates suggestions to optimize a resume for a specific job."""
        prompt = f"""
        Act as a professional resume writer. Optimize the resume data for the given job description.
        Your response MUST be a single, valid JSON object and nothing else.

        Current Resume Data: {json.dumps(resume_data)}
        Job Description: {job_description}

        Return a single JSON object with this structure:
        {{
            "optimized_summary": "An enhanced professional summary, tailored to the job.",
            "missing_keywords": ["A list of critical keywords to add to the skills section."]
        }}
        """
        response_text = self._safe_generate_content(prompt)
        return self._extract_json(response_text)
    
    def generate_course_recommendations(self, skills, job_description):
        """Generates a list of course recommendations based on skill gaps."""
        prompt = f"""
        Act as a career development advisor. Recommend 3-5 specific online courses to bridge skill gaps based on the user's skills and the job description.
        Your response MUST be a single, valid JSON array of objects and nothing else.

        Current Skills: {', '.join(skills)}
        Job Requirements: {job_description}

        Return a JSON array where each object has this structure:
        {{
            "course_name": "Course Title", "provider": "Platform (e.g., Coursera, Udemy)",
            "reason": "Why this course is recommended.",
            "skill_gap": "The specific skill this course addresses.",
            "duration": "Estimated time to complete."
        }}
        """
        response_text = self._safe_generate_content(prompt)
        return self._extract_json(response_text, start_char='[', end_char=']')
        
    def generate_interview_questions(self, job_description, resume_data):
        """Generates personalized interview questions."""
        prompt = f"""
        Act as a hiring manager. Based on the job description and resume, generate 10-15 tailored interview questions.
        Categorize them into "General", "Technical", and "Behavioral".
        Your response MUST be a single, valid JSON array of objects and nothing else.

        Job Description: {job_description}
        Candidate Resume: {json.dumps(resume_data)}

        Return a JSON array where each object has this structure:
        {{
            "question": "The full text of the question.",
            "category": "General, Technical, or Behavioral",
            "tips": "A brief tip on how to best answer this question."
        }}
        """
        response_text = self._safe_generate_content(prompt)
        return self._extract_json(response_text, start_char='[', end_char=']')

    def evaluate_interview_answer(self, question, answer, job_description):
        """Evaluates a candidate's answer to an interview question."""
        prompt = f"""
        Act as a professional career coach. Evaluate the interview answer in the context of the job description.
        Provide constructive, concise feedback. Your response MUST be ONLY in Markdown format using the exact headings specified below.
        
        Job Description Context: {job_description}
        Interview Question: "{question}"
        Candidate's Answer: "{answer}"

        Structure your feedback with these exact headings:
        - **Overall Score:** (Provide a score out of 10)
        - **✅ What Went Well:** (List 2 specific strengths)
        - **🔧 Areas for Improvement:** (List 2 specific, actionable suggestions)
        - **⭐ A Stronger Example Answer:** (Rewrite the user's answer to be more impactful)
        """
        return self._safe_generate_content(prompt) or "Feedback could not be generated."

    def generate_cover_letter(self, resume_data, job_description):
        """Generates a compelling cover letter."""
        prompt = f"""
        Based on the provided resume and job description, write a professional and compelling cover letter.
        Personalize it to the candidate's experience and directly address the job requirements.
        Maintain a confident and professional tone. The letter should not exceed 400 words.

        Resume Data: {json.dumps(resume_data)}
        Job Description: {job_description}
        """
        return self._safe_generate_content(prompt) or "Cover letter could not be generated."

    def generate_linkedin_summary(self, resume_data):
        """Generates an engaging LinkedIn 'About' section summary."""
        prompt = f"""
        Based on the provided resume, write an engaging, first-person LinkedIn 'About' section summary.
        It should be professional yet approachable, starting with a strong hook.
        Highlight key skills and quantifiable achievements. End with a call to action.

        Resume Data: {json.dumps(resume_data)}
        """
        return self._safe_generate_content(prompt) or "LinkedIn summary could not be generated."
    def create_enhanced_pdf_resume(resume_data, template_style="professional"):
        """
        Generates an enhanced PDF resume with multiple template options.
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.75*inch, bottomMargin=0.75*inch)
        styles = getSampleStyleSheet()
        story = []

        # --- Template-based Styling ---
        if template_style == "modern":
            primary_color = colors.HexColor('#1E90FF')
        elif template_style == "creative":
            primary_color = colors.HexColor('#8E44AD')
        else:  # professional
            primary_color = colors.HexColor('#000080')

        # --- Custom Styles ---
        name_style = ParagraphStyle('NameStyle', parent=styles['h1'], fontSize=24, textColor=primary_color, alignment=1, spaceAfter=6)
        contact_style = ParagraphStyle('ContactStyle', parent=styles['Normal'], fontSize=10, alignment=1, spaceAfter=12)
        section_style = ParagraphStyle('SectionStyle', parent=styles['h2'], fontSize=14, textColor=primary_color, fontName='Helvetica-Bold', spaceBefore=12, spaceAfter=6, borderBottomWidth=1, borderBottomColor=primary_color, paddingBottom=2)
    
        # FIX 1: Create a dedicated style for bullet points with indentation.
        bullet_style = ParagraphStyle('BulletStyle', parent=styles['Normal'], leftIndent=20, spaceAfter=6)
    
        # --- Build Document Story ---
        story.append(Paragraph(resume_data.get('name', 'Your Name'), name_style))
        story.append(Paragraph(f"{resume_data.get('email', '')} | {resume_data.get('phone', '')}", contact_style))

        sections = {
            "summary": "Professional Summary", "skills": "Core Competencies", "experience": "Professional Experience",
            "education": "Education", "projects": "Key Projects", "certifications": "Certifications"
        }

        for key, title in sections.items():
            if resume_data.get(key):
                story.append(Paragraph(title.upper(), section_style))
                content = resume_data[key]
                if isinstance(content, list):
                    if key == 'skills':
                        skill_rows = [content[i:i+3] for i in range(0, len(content), 3)]
                        story.append(Table(skill_rows, colWidths=[2.2*inch, 2.2*inch, 2.2*inch], style=[('VALIGN', (0,0), (-1,-1), 'TOP')]))
                    else:
                        for item in content:
                            # FIX 2: Use the new 'bullet_style' here.
                            story.append(Paragraph(f"• {item}", bullet_style))
                else:
                    story.append(Paragraph(content, styles['Normal']))

        doc.build(story)
        buffer.seek(0)
        return buffer