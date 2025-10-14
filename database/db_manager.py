import sqlite3
import bcrypt
import json
import datetime

# --- CONSTANTS ---
DB_NAME = "resume_optimizer.db"

# --- DATABASE INITIALIZATION ---
def init_db():
    """
    Initializes the database and creates the 'users' and 'resumes' tables
    if they do not already exist.
    """
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        
        # Create users table for login credentials
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
        """)
        
        # Create resumes table to store user history
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            resume_data TEXT NOT NULL,
            job_description TEXT,
            ats_score REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """)
        conn.commit()

# --- PASSWORD MANAGEMENT ---
def hash_password(password: str) -> str:
    """Hashes a password using bcrypt for secure storage."""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def verify_password(stored_hash: str, provided_password: str) -> bool:
    """Verifies a provided password against a stored bcrypt hash."""
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_hash.encode('utf-8'))

# --- USER MANAGEMENT ---
def add_user(username, password):
    """
    Adds a new user to the database. Hashes the password before storing.
    Returns True on success, False if the username already exists.
    """
    conn = sqlite3.connect(DB_NAME)
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                       (username, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:  # This error occurs if the username is not unique
        return False
    finally:
        conn.close()

def authenticate_user(username, password):
    """
    Authenticates a user. Returns the user's ID if credentials are valid,
    otherwise returns None.
    """
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,))
        user_record = cursor.fetchone()
        
        if user_record and verify_password(user_record[1], password):
            return user_record[0]  # Return user ID on successful authentication
    return None

# --- RESUME HISTORY MANAGEMENT ---
def save_resume(user_id, resume_data, job_description, ats_score):
    """
    Saves a user's resume analysis to the database. The resume_data dictionary
    is stored as a JSON string.
    """
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO resumes (user_id, resume_data, job_description, ats_score)
        VALUES (?, ?, ?, ?)
        """, (user_id, json.dumps(resume_data), job_description, ats_score))
        conn.commit()

def get_user_resumes(user_id):
    """
    Retrieves all saved resume analyses for a given user, ordered by most recent.
    """
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT resume_data, job_description, ats_score, created_at FROM resumes
        WHERE user_id = ? ORDER BY created_at DESC
        """, (user_id,))
        resumes = cursor.fetchall()
        
        # Parse the JSON data from text back into a dictionary
        parsed_resumes = []
        for row in resumes:
            parsed_resumes.append({
                "resume_data": json.loads(row[0]),
                "job_description": row[1],
                "ats_score": row[2],
                "created_at": row[3]
            })
        return parsed_resumes