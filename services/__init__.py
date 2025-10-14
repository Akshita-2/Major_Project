# services/__init__.py

from .ai_services import GeminiAIHelper
from .file_processors import (
    extract_text_from_pdf,
    extract_text_from_docx,
    process_voice_input,
    process_video_resume
)
from .resume_generator import (
    create_enhanced_pdf_resume,
    create_word_resume,
    create_html_resume,
    create_resume_package
)

# Explicitly define the public API of the 'services' package.
# When another module uses 'from services import *', only these names will be imported.
__all__ = [
    "GeminiAIHelper",
    "extract_text_from_pdf",
    "extract_text_from_docx",
    "process_voice_input",
    "process_video_resume",
    "create_enhanced_pdf_resume",
    "create_word_resume",
    "create_html_resume",
    "create_resume_package"
]