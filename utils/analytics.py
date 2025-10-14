import datetime

def calculate_completion_score(resume_data):
    """
    Calculates a "completion score" for the resume based on filled sections.

    Args:
        resume_data (dict): The structured resume data.

    Returns:
        A float representing the completion percentage (0-100).
    """
    if not resume_data:
        return 0.0

    # Define the most important fields for a complete resume
    required_fields = [
        'name', 'email', 'phone', 'summary', 
        'skills', 'experience', 'education'
    ]
    
    completed_fields = sum(1 for field in required_fields if resume_data.get(field))
    
    try:
        score = (completed_fields / len(required_fields)) * 100
    except ZeroDivisionError:
        score = 0.0
        
    return score

def generate_analytics_report(resume_data, ats_score=0):
    """
    Generates a comprehensive, plain-text analytics report.

    Args:
        resume_data (dict): The structured resume data.
        ats_score (float): The ATS score from the analysis.

    Returns:
        A formatted string containing the full report.
    """
    completion = calculate_completion_score(resume_data)
    
    report = f"""
RESUME ANALYTICS REPORT
==================================================
Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## COMPLETION ANALYSIS ##
--------------------------------------------------
Overall Completion: {completion:.1f}%
- Skills Listed: {len(resume_data.get('skills', []))}
- Experience Entries: {len(resume_data.get('experience', []))}
- Education Entries: {len(resume_data.get('education', []))}
- Projects Listed: {len(resume_data.get('projects', []))}

## ATS OPTIMIZATION ##
--------------------------------------------------
Current ATS Score: {ats_score:.1f}%
Recommended Score for competitive applications: 85%+

## KEYWORD ANALYSIS (Sample) ##
--------------------------------------------------
This section would contain a more detailed breakdown of technical vs. soft skills
found in a full implementation.
- Total Keywords/Skills Found: {len(resume_data.get('skills', []))}

## GENERAL RECOMMENDATIONS ##
--------------------------------------------------
1.  **Quantify Achievements:** Instead of "managed a team," use "managed a team of 5 engineers to increase productivity by 15%."
2.  **Tailor Keywords:** Always adapt the skills and summary to match the keywords in the specific job description you are targeting.
3.  **Action Verbs:** Start each bullet point in your experience section with a strong action verb (e.g., "Orchestrated," "Engineered," "Maximized").
4.  **Formatting:** Ensure consistent formatting (dates, titles, etc.) throughout the document. Simpler, single-column layouts are generally more ATS-friendly.

## NEXT STEPS ##
--------------------------------------------------
- Use the 'Download' page to get a professionally formatted PDF.
- Use the 'Interview Prep' tool to practice with AI-generated questions.
- Save this analysis to your history to track your improvements over time.

--- End of Report ---
    """
    return report.strip()