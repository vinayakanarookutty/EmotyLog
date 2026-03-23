import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret')
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/ai_diary_db')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')