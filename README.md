


Project: AI Soul Diary (Flask + MongoDB + Three.js)
This is a Flask-based web application featuring a futuristic 3D UI, AI emotion detection, voice input, and time-travel simulation for examiners.

1. Prerequisites
Before running the app, ensure you have the following installed:

Python 3.8+

MongoDB Community Server (Must be running locally)

Download MongoDB Here

Google Gemini API Key

Get Free Key Here

2. Installation
Step 1: Create the Project Folder
If you haven't already, create the folder structure:

Bash
mkdir diary_project
cd diary_project
Step 2: Set Up a Virtual Environment (Recommended)
It is best practice to use a virtual environment to keep dependencies clean.

Windows:

Bash
python -m venv venv
venv\Scripts\activate
Mac/Linux:

Bash
python3 -m venv venv
source venv/bin/activate
Step 3: Install Dependencies
Run this command to install all required libraries:

Bash
pip install -r requirements.txt
pip install flask flask-pymongo flask-bcrypt google-generativeai python-dotenv pillow
3. Configuration
Create a file named .env in the root folder (diary_project/.env) and add your configuration:

Ini, TOML
# .env file content
GEMINI_API_KEY=PASTE_YOUR_GOOGLE_API_KEY_HERE
SECRET_KEY=my_super_secret_key_change_this
MONGO_URI=mongodb://localhost:27017/ai_diary_db
4. Running the Application
Make sure MongoDB is running in the background.

Windows: Open Task Manager/Services or run mongod in a separate terminal.

Mac/Linux: brew services start mongodb-community

Run the Flask application:

Bash
python run.py
Open your browser and go to:
http://127.0.0.1:5000

5. Project Structure
Your project should look like this:

Plaintext
/diary_project
│
├── run.py                 # ENTRY POINT (Run this file)
├── .env                   # API Keys (Create this manually)
│
└── /app
    ├── __init__.py        # App Factory
    ├── config.py          # Config Loader
    ├── extensions.py      # DB & Bcrypt Setup
    ├── utils.py           # AI & Helper Functions
    │
    ├── /routes
    │   ├── __init__.py
    │   ├── auth.py        # Login/Register Routes
    │   ├── main.py        # Dashboard/Write/Chat Routes
    │   └── api.py         # AI API Endpoints
    │
    └── /templates
        ├── layout.html    # Main 3D Template
        ├── login.html     # Login Page
        ├── register.html  # Register Page
        ├── dashboard.html # Main Hub
        ├── write.html     # Writing Interface
        └── chat.html      # AI Chat Interface
6. Troubleshooting
Error: ModuleNotFoundError: No module named 'flask'

You forgot to activate your virtual environment or run pip install. Check Step 2.

Error: ConnectionRefusedError: [Errno 111] Connection refused

MongoDB is not running. Start MongoDB manually.

Error: 400 Bad Request: Key not found

Check your .env file. Make sure your GEMINI_API_KEY is correct.

7. Examiner Demo Guide
To demonstrate the features to an examiner:

Sign Up using the 3D Register page.

Write a Diary Entry using Voice Input.

Edit the Entry to show it works.

Use "Time Travel" on the Dashboard (Left Panel). Change the date to 3 days in the future.

Refresh: Show that the previous entry is now Locked.

Weekly Story: Add 2 more entries, then click "Generate Weekly Saga".