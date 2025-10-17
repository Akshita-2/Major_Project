# 🚀 Hiredly - Your AI Career Co-Pilot

Streamline your job application process with an AI-powered suite that analyzes, optimizes, and prepares you for your next big opportunity. Built with Streamlit and powered by Google's Gemini AI.


---

## ✨ About The Project

Hiredly is a smart, fast, and beautiful web application designed to give job seekers a competitive edge. It moves beyond simple keyword matching by leveraging a powerful AI agent to perform a comprehensive, one-click analysis of your resume against a target job description.

The "analyze-once, explore-instantly" architecture ensures a seamless user experience. After a single processing step, all insights—from ATS compatibility to personalized interview questions—are available instantly across the app.

---

## 🛠️ Key Features

* **Multi-Format Resume Parsing:** Input your resume via text, PDF, DOCX, live voice recording, or video upload.
* **🚀 Instant "Analyze-Once" Workflow:** All AI tasks (ATS, optimization, interview prep, etc.) are run in a single, upfront step for a lightning-fast user experience.
* **📊 Detailed ATS Analysis:** Get a comprehensive ATS score with a breakdown of keyword matches, content relevance, and formatting.
* **🤖 Automatic Optimization:** The AI agent automatically enhances your resume summary and adds missing keywords based on the job description.
* **🎓 Personalized Course Recommendations:** Identifies skill gaps and suggests specific online courses to bridge them.
* **🎤 AI Mock Interview Simulator:** Practice with tailored interview questions and get instant, structured feedback on your answers using text or voice.
* **📄 Multi-Format Resume Downloads:** Download your polished, AI-optimized resume in various templates as a PDF, DOCX, or a complete ZIP package.
* **🔒 Secure User Accounts & History:** User accounts are securely managed, and all past analysis sessions are saved for future reference.

---

## 📚 Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/)
* **AI Model:** [Google Gemini Pro](https://deepmind.google/technologies/gemini/)
* **Database:** [SQLite](https://www.sqlite.org/index.html)
* **PDF Generation:** [ReportLab](https://www.reportlab.com/)
* **File Processing:** PyPDF2, python-docx, moviepy, pydub, SpeechRecognition
* **Data Visualization:** Plotly, Matplotlib

---

## ⚙️ Getting Started

Follow these steps to get a local copy up and running.

### Prerequisites

This project requires a few external dependencies that are not installed via `pip`.

* **FFmpeg** (for video processing)
    * **Windows:** [Installation Guide](https://www.geeksforgeeks.org/how-to-install-ffmpeg-on-windows/)
    * **Mac:** `brew install ffmpeg`
    * **Linux:** `sudo apt update && sudo apt install ffmpeg`

* **PortAudio** (for microphone access via `PyAudio`)
    * **Mac:** `brew install portaudio`
    * **Linux:** `sudo apt-get install portaudio19-dev`

### Installation

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/your-username/hiredly.git](https://github.com/your-username/hiredly.git)
    cd hiredly
    ```

2.  **Create and activate a virtual environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required Python packages:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Set up your API Key:**
    * Create a folder named `.streamlit` in the root directory.
    * Inside `.streamlit`, create a file named `secrets.toml`.
    * Add your Google Gemini API key to this file:
        ```toml
        # .streamlit/secrets.toml
        GEMINI_API_KEY = "YOUR_API_KEY_HERE"
        ```

---

## 🚀 Usage

1.  **Run the application:**
    ```sh
    streamlit run main.py
    ```

2.  **Follow the workflow:**
    * Create an account or log in.
    * On the **Dashboard**, provide your resume (via text, file, voice, or video) and the target job description.
    * Click the **"Analyze & Prepare"** button and wait for the AI to complete its multi-step analysis.
    * Once complete, navigate to the other pages (ATS Analysis, Course Recommendations, etc.) to instantly view your personalized results!

---



