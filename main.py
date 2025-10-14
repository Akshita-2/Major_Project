import streamlit as st
import datetime
from database import init_db, authenticate_user, add_user, get_user_resumes
from utils.session_state import initialize_session_state

# --- 1. PAGE CONFIGURATION ---
# This must be the first Streamlit command in your script.
st.set_page_config(
    page_title="Hiredly",
    page_icon="🚀",  # New icon for Hiredly
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. DATABASE INITIALIZATION ---
# Ensures the database and tables are created when the app starts.
init_db()

# --- 3. AUTHENTICATION UI ---
def show_login_page():
    """Displays the login form."""
    st.title("🚀 Hiredly: Your AI Career Co-Pilot")
    st.header("Login")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        
        if submitted:
            user_id = authenticate_user(username, password)
            if user_id:
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.session_state['user_id'] = user_id
                st.toast(f"Welcome back, {username}!", icon="👋")
                st.rerun()  # Rerun the script to reflect the logged-in state
            else:
                st.error("Invalid username or password")

def show_signup_page():
    """Displays the sign-up form."""
    st.title("🚀 Hiredly: Your AI Career Co-Pilot")
    st.header("Sign Up")
    with st.form("signup_form"):
        new_username = st.text_input("Choose a Username")
        new_password = st.text_input("Choose a Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submitted = st.form_submit_button("Sign Up")
        
        if submitted:
            if not all([new_username, new_password, confirm_password]):
                st.error("Please fill out all fields.")
            elif new_password == confirm_password:
                if add_user(new_username, new_password):
                    st.success("Account created successfully! Please log in.")
                else:
                    st.error("Username already exists. Please choose another.")
            else:
                st.error("Passwords do not match.")

# --- 4. POST-LOGIN UI ---
def show_history_page():
    """Displays the user's saved resume analyses."""
    st.header(f"📜 {st.session_state.username}'s History")
    st.markdown("Here are your previously saved resume analyses, with the most recent first.")
    
    resumes = get_user_resumes(st.session_state['user_id'])
    if not resumes:
        st.info("You have no saved analyses yet. Perform an analysis on the Dashboard to save it here.")
    else:
        for res in resumes:
            date = datetime.datetime.strptime(res['created_at'], '%Y-%m-%d %H:%M:%S').strftime('%B %d, %Y')
            expander_title = f"Analysis from {date} - ATS Score: {res['ats_score']:.1f}%"
            
            with st.expander(expander_title):
                st.subheader("Resume Data Snapshot")
                st.json(res['resume_data'])
                st.subheader("Target Job Description")
                st.code(res['job_description'], language='text')

def main_app():
    """The main application view after a user has logged in."""
    # Initialize the session state for the optimizer tools
    initialize_session_state()

    # --- Sidebar Navigation for Account ---
    st.sidebar.title(f"Welcome, {st.session_state.username}!")
    
    st.sidebar.markdown("---")
    page_selection = st.sidebar.radio("My Account", ["Hiredly Tools", "My History", "Logout"])
    st.sidebar.markdown("---")

    # --- Page Content ---
    if page_selection == "Hiredly Tools":
        st.title("🚀 Welcome to Hiredly")
        st.markdown("""
        Select a tool from the navigation panel on the left to begin. 
        Start with the **Dashboard** to input your resume and let the AI do the work!
        """)
        st.info("The new workflow is now active: Analyze once on the Dashboard, then explore the results instantly on the other pages.")

    elif page_selection == "My History":
        show_history_page()
        
    elif page_selection == "Logout":
        # Clear the entire session state to log out
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# --- 5. MAIN CONTROL FLOW ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if st.session_state['logged_in']:
    main_app()
else:
    choice = st.selectbox("Login or Sign Up", ["Login", "Sign Up"], label_visibility="collapsed")
    if choice == "Login":
        show_login_page()
    else:
        show_signup_page()