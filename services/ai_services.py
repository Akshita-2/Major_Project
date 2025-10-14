import streamlit as st
import json

class GeminiAIHelper:
    """
    A service class to handle all interactions with the Google Gemini API.
    It abstracts the prompt engineering and API call logic away from the UI.
    """
    
    def __init__(self, model):
        """
        Initializes the helper with a configured Gemini model instance.
        
        Args:
            model: An instance of a google.generativeai.GenerativeModel.
        """
        self.model = model

    def _safe_generate_content(self, prompt):
        """A wrapper for API calls to handle potential errors."""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            st.error(f"An error occurred with the AI service: {e}")
            return None

    def _extract_json(self, text, start_char='{', end_char='}'):
        """
        Safely extracts a JSON object or array from a string.
        
        Args:
            text (str): The text potentially containing a JSON object.
            start_char (str): The starting character of the JSON structure ('{' or '[').
            end_char (str): The ending character of the JSON structure ('}' or ']').

        Returns:
            dict or list: The parsed JSON object, or an empty dict/list on failure.
        """
        try:
            start_index = text.find(start_char)
            end_index = text.rfind(end_char)
            if start_index != -1 and end_index != -1:
                json_str = text[start_index : end_index + 1]
                return json.loads(json_str)
        except (json.JSONDecodeError, IndexError) as e:
            st.warning(f"Could not parse AI response. Using fallback. Error: {e}")
        
        return {} if start_char == '{' else []

    def analyze_resume_content(self, resume_text):
        """Uses Gemini to parse raw resume text into a structured JSON object."""
        prompt = f"""
        Analyze the following resume text and extract structured information in JSON format.
        Be thorough. If a section is missing, provide an empty list or string.

        Resume Text:
        ---
        {resume_text}
        ---

        Return a single JSON object with the following structure:
        {{
            "name": "string",
            "email": "string",
            "phone": "string",
            "summary": "string",
            "skills": ["list", "of", "skills"],
            "experience": ["list of detailed work experience entries"],
            "education": ["list of education entries"],
            "certifications": ["list of certifications, if any"],
            "projects": ["list of projects, if any"]
        }}
        """
        response_text = self._safe_generate_content(prompt)
        return self._extract_json(response_text) if response_text else {}

    def score_resume_ats(self, resume_text, job_description):
        """Provides a detailed ATS analysis and score as a JSON object."""
        prompt = f"""
        Act as an expert ATS (Applicant Tracking System). Analyze the resume against the job description.
        Provide a detailed analysis as a JSON object.

        Resume:
        ---
        {resume_text}
        ---
        Job Description:
        ---
        {job_description}
        ---

        Return a single JSON object with this structure:
        {{
            "ats_score": number between 0 and 100,
            "keyword_match_percentage": number between 0 and 100,
            "missing_critical_keywords": ["list of important missing keywords"],
            "strengths": ["list of what the resume does well"],
            "improvement_areas": ["list of specific areas to improve"],
            "formatting_score": number between 0 and 100,
            "content_relevance_score": number between 0 and 100
        }}
        """
        response_text = self._safe_generate_content(prompt)
        return self._extract_json(response_text) if response_text else {}

    def optimize_resume_for_job(self, resume_data, job_description):
        """Generates suggestions to optimize a resume for a specific job."""
        prompt = f"""
        Act as a professional resume writer. Optimize the resume data for the given job description.
        Provide your response as a JSON object.

        Current Resume Data: {json.dumps(resume_data, indent=2)}
        Job Description: {job_description}

        Return a single JSON object with this structure:
        {{
            "optimized_summary": "An enhanced professional summary, tailored to the job.",
            "missing_keywords": ["A list of critical keywords to add to the skills section."],
            "improvement_suggestions": ["A list of overall improvement suggestions."]
        }}
        """
        response_text = self._safe_generate_content(prompt)
        return self._extract_json(response_text) if response_text else {}
    
    def generate_course_recommendations(self, skills, job_description):
        """Generates a list of course recommendations based on skill gaps."""
        prompt = f"""
        Act as a career development advisor. Based on the candidate's current skills and the job requirements, 
        recommend 3 to 5 specific online courses to bridge any skill gaps.

        Current Skills: {', '.join(skills)}
        Job Requirements: {job_description}

        Return a JSON array where each object has this structure:
        {{
            "course_name": "Course Title",
            "provider": "Platform (e.g., Coursera, Udemy)",
            "reason": "Why this course is recommended for the user.",
            "skill_gap": "The specific skill this course addresses.",
            "duration": "Estimated time to complete."
        }}
        """
        response_text = self._safe_generate_content(prompt)
        return self._extract_json(response_text, start_char='[', end_char=']') if response_text else []
        
    def generate_interview_questions(self, job_description, resume_data):
        """Generates personalized interview questions."""
        prompt = f"""
        Act as a hiring manager. Based on the job description and candidate's resume, generate 10-15 tailored interview questions.
        Categorize the questions into "General", "Technical", and "Behavioral".

        Job Description: {job_description}
        Candidate Resume: {json.dumps(resume_data, indent=2)}

        Return a JSON array where each object has this structure:
        {{
            "question": "The full text of the question.",
            "category": "General, Technical, or Behavioral",
            "tips": "A brief tip on how to best answer this question."
        }}
        """
        response_text = self._safe_generate_content(prompt)
        return self._extract_json(response_text, start_char='[', end_char=']') if response_text else []

    def evaluate_interview_answer(self, question, answer, job_description):
        """Evaluates a candidate's answer to an interview question."""
        prompt = f"""
        Act as a professional career coach. Evaluate the following interview answer in the context of the job description.

        Job Description Context: {job_description}
        Interview Question: "{question}"
        Candidate's Answer: "{answer}"

        Provide constructive, concise feedback in Markdown format. Structure your feedback with these exact headings:
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
        Personalize it to the candidate's experience and directly address the requirements in the job description.
        Maintain a confident and professional tone. The letter should not exceed 400 words.

        Resume Data: {json.dumps(resume_data, indent=2)}
        Job Description: {job_description}
        """
        return self._safe_generate_content(prompt) or "Cover letter could not be generated."

    def generate_linkedin_summary(self, resume_data):
        """Generates an engaging LinkedIn 'About' section summary."""
        prompt = f"""
        Based on the provided resume, write an engaging, first-person LinkedIn 'About' section summary.
        It should be professional yet approachable, starting with a strong hook.
        Highlight key skills and quantifiable achievements. End with a call to action.

        Resume Data: {json.dumps(resume_data, indent=2)}
        """
        return self._safe_generate_content(prompt) or "LinkedIn summary could not be generated."