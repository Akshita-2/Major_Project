# database/__init__.py

from .db_manager import (
    init_db,
    add_user,
    authenticate_user,
    save_resume,
    get_user_resumes
)

# Explicitly define the public API of the 'database' package
__all__ = [
    "init_db",
    "add_user",
    "authenticate_user",
    "save_resume",
    "get_user_resumes"
]