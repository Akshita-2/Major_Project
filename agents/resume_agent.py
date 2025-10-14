import streamlit as st
from services.ai_services import GeminiAIHelper

class ResumeAgent:
    """
    An AI agent that acts as a co-pilot for career tasks.
    It can run a full analysis workflow or execute specific, ad-hoc tasks.
    """
    
    def __init__(self):
        """Initializes the agent with its toolbox of AI functions."""
        if 'gemini_model' not in st.session_state:
            st.error("Gemini model not initialized. Please log in again.")
            return
            
        self.ai_helper = GeminiAIHelper(st.session_state.gemini_model)
        
        # The "toolbox" contains all the functions the agent can decide to use.
        self.tools = {
            "optimize_resume": self.ai_helper.optimize_resume_for_job,
            "generate_questions": self.ai_helper.generate_interview_questions,
            "score_ats": self.ai_helper.score_resume_ats,
            "evaluate_answer": self.ai_helper.evaluate_interview_answer,
            "recommend_courses": self.ai_helper.generate_course_recommendations,
        }

    def run_full_analysis(self, resume_data, job_description):
        """
        NEW: Runs the complete, sequential analysis for the main dashboard.
        This is the core of the "analyze-once" workflow.
        """
        all_results = {}
        resume_text = " ".join(map(str, [
            resume_data.get('summary', ''),
            " ".join(map(str, resume_data.get('skills', []))),
            " ".join(map(str, resume_data.get('experience', []))),
        ]))

        # --- Step 1: ATS Score and Optimization ---
        st.info("Step 1/3: Analyzing ATS compatibility and finding optimizations...")
        all_results['ats'] = self.tools["score_ats"](resume_text, job_description)
        all_results['optimization'] = self.tools["optimize_resume"](resume_data, job_description)

        # --- Step 2: Generate Interview Questions ---
        st.info("Step 2/3: Crafting personalized interview questions...")
        all_results['questions'] = self.tools["generate_questions"](job_description, resume_data)

        # --- Step 3: Recommend Courses ---
        st.info("Step 3/3: Identifying skill gaps and recommending courses...")
        skills = resume_data.get('skills', [])
        all_results['courses'] = self.tools["recommend_courses"](skills, job_description)

        st.success("Full analysis complete!")
        return all_results


    def execute_task(self, task_description: str, resume_data: dict, job_description: str, **kwargs):
        """
        Executes a single, specific task based on a user's text command.
        Used by the interactive sidebar assistant.
        """
        task = task_description.lower()

        # Router Logic: Simple keyword matching to select the right tool.
        if "summary" in task or "optimize" in task or "improve" in task:
            st.info("Agent is optimizing your resume...")
            return self.tools["optimize_resume"](resume_data, job_description)

        elif "interview" in task or "question" in task:
            st.info("Agent is generating interview questions...")
            return self.tools["generate_questions"](job_description, resume_data)
        
        elif "evaluate" in task or "feedback" in task:
            question = kwargs.get('question')
            answer = kwargs.get('answer')
            if not question or not answer:
                return "To evaluate an answer, I need both the question and your answer."
            st.info("Agent is evaluating your answer...")
            return self.tools["evaluate_answer"](question, answer, job_description)
            
        else:
            return {"error": "I'm sorry, I don't have a tool for that task. Please try asking me to 'optimize your resume' or 'prepare for an interview'."}