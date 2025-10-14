import json
import datetime
import zipfile
from io import BytesIO

# --- ReportLab for PDF Generation ---
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

# --- python-docx for Word Document Generation ---
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH


def create_enhanced_pdf_resume(resume_data, template_style="professional"):
    """
    Generates an enhanced PDF resume with multiple template options.

    Args:
        resume_data (dict): The structured resume data.
        template_style (str): The visual theme ('professional', 'modern', 'creative').

    Returns:
        A BytesIO buffer containing the generated PDF file.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.75*inch, bottomMargin=0.75*inch)
    styles = getSampleStyleSheet()
    story = []

    # --- Template-based Styling ---
    if template_style == "modern":
        primary_color = colors.HexColor('#2E86C1')
        section_font = 'Helvetica-Bold'
    elif template_style == "creative":
        primary_color = colors.HexColor('#8E44AD')
        section_font = 'Helvetica-Bold'
    else:  # professional
        primary_color = colors.HexColor('#000080') # Navy Blue
        section_font = 'Helvetica-Bold'

    # --- Custom Styles ---
    name_style = ParagraphStyle('NameStyle', parent=styles['h1'], fontSize=24, textColor=primary_color, alignment=1, spaceAfter=6)
    contact_style = ParagraphStyle('ContactStyle', parent=styles['Normal'], fontSize=10, alignment=1, spaceAfter=12)
    section_style = ParagraphStyle('SectionStyle', parent=styles['h2'], fontSize=14, textColor=primary_color, fontName=section_font, spaceBefore=12, spaceAfter=6, borderBottomWidth=1, borderBottomColor=primary_color, paddingBottom=2)
    
    # --- Build Document Story ---
    story.append(Paragraph(resume_data.get('name', 'Your Name'), name_style))
    contact_info = f"{resume_data.get('email', '')} | {resume_data.get('phone', '')}"
    story.append(Paragraph(contact_info, contact_style))

    sections = ["summary", "skills", "experience", "education", "projects", "certifications"]
    section_titles = {
        "summary": "Professional Summary", "skills": "Core Competencies", "experience": "Professional Experience",
        "education": "Education", "projects": "Key Projects", "certifications": "Certifications"
    }

    for section in sections:
        if resume_data.get(section):
            story.append(Paragraph(section_titles[section].upper(), section_style))
            if isinstance(resume_data[section], list):
                if section == 'skills':
                    # Format skills into a multi-column table
                    skills = resume_data['skills']
                    skill_rows = [skills[i:i+3] for i in range(0, len(skills), 3)]
                    skills_table = Table(skill_rows, colWidths=[2.2*inch, 2.2*inch, 2.2*inch])
                    skills_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
                    story.append(skills_table)
                else:
                    for item in resume_data[section]:
                        story.append(Paragraph(f"• {item}", styles['Normal'], bulletIndent=10))
            else: # For summary string
                story.append(Paragraph(resume_data[section], styles['Normal']))

    doc.build(story)
    buffer.seek(0)
    return buffer


def create_word_resume(resume_data):
    """
    Generates a Word document (.docx) from the resume data.
    """
    doc = Document()
    doc.add_heading(resume_data.get('name', 'Your Name'), 0).alignment = WD_ALIGN_PARAGRAPH.CENTER
    contact_info = f"{resume_data.get('email', '')} | {resume_data.get('phone', '')}"
    doc.add_paragraph(contact_info).alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    sections = {
        "Professional Summary": "summary", "Core Skills": "skills", "Professional Experience": "experience",
        "Education": "education", "Key Projects": "projects", "Certifications": "certifications"
    }

    for title, key in sections.items():
        if resume_data.get(key):
            doc.add_heading(title.upper(), level=1)
            content = resume_data[key]
            if isinstance(content, list):
                for item in content:
                    doc.add_paragraph(item, style='List Bullet')
            else:
                doc.add_paragraph(content)

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer


def create_html_resume(resume_data):
    """
    Generates a single-file HTML resume.
    """
    skills_html = ''.join([f'<span class="skill-tag">{skill}</span>' for skill in resume_data.get('skills', [])])
    experience_html = ''.join([f'<li>{exp}</li>' for exp in resume_data.get('experience', [])])
    
    html_template = f"""
    <!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>{resume_data.get('name', 'Resume')}</title>
    <style>body{{font-family: Arial, sans-serif; max-width: 800px; margin: auto; padding: 20px; line-height: 1.6;}} .name{{font-size: 2.5em; color: #2E86C1; text-align: center;}} .contact{{text-align: center; color: #555; margin-bottom: 20px;}} .section-title{{font-size: 1.4em; color: #2E86C1; border-bottom: 2px solid #2E86C1; padding-bottom: 5px; margin-top: 20px;}} .skill-tag{{display: inline-block; background: #2E86C1; color: white; padding: 5px 12px; border-radius: 15px; margin: 5px; font-size: 0.9em;}} ul{{padding-left: 20px;}}</style></head>
    <body>
        <div class="name">{resume_data.get('name', '')}</div>
        <div class="contact">{resume_data.get('email', '')} | {resume_data.get('phone', '')}</div>
        <div class="section-title">Professional Summary</div><p>{resume_data.get('summary', '')}</p>
        <div class="section-title">Core Skills</div><div>{skills_html}</div>
        <div class="section-title">Experience</div><ul>{experience_html}</ul>
    </body></html>
    """
    return html_template.encode('utf-8')


def create_resume_package(resume_data, template_style):
    """
    Creates a ZIP file containing the resume in multiple formats (PDF, DOCX, HTML, JSON).
    """
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # 1. Add PDF resume
        pdf_buffer = create_enhanced_pdf_resume(resume_data, template_style)
        zip_file.writestr("resume.pdf", pdf_buffer.getvalue())

        # 2. Add Word resume
        word_buffer = create_word_resume(resume_data)
        zip_file.writestr("resume.docx", word_buffer.getvalue())

        # 3. Add HTML resume
        html_content = create_html_resume(resume_data)
        zip_file.writestr("resume.html", html_content)
        
        # 4. Add JSON data backup
        json_content = json.dumps(resume_data, indent=2)
        zip_file.writestr("resume_data.json", json_content)

        # 5. Add a README file
        readme_content = f"""
        AI Resume Package
        ====================
        Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

        This package contains your AI-optimized resume in multiple formats:
        - resume.pdf: Professional PDF format, best for applications.
        - resume.docx: Editable Word document.
        - resume.html: Web-ready HTML version.
        - resume_data.json: Your resume data in a machine-readable format for backup.
        """
        zip_file.writestr("README.txt", readme_content.strip())
    
    zip_buffer.seek(0)
    return zip_buffer.getvalue()