import datetime
from flask import session
import google.generativeai as genai
from PIL import Image

# Time Travel Helper
def get_current_date():
    if 'simulated_date' in session:
        return datetime.datetime.strptime(session['simulated_date'], "%Y-%m-%d")
    return datetime.datetime.now()

# AI Analysis Helper
def get_ai_emotion_and_motivation(text):
    model = genai.GenerativeModel('gemini-2.5-flash')
    prompt = f"Analyze this diary entry: '{text}'. 1. Identify the core emotion (one word). 2. Write a short, powerful motivational quote. Format: Emotion|Quote"
    try:
        response = model.generate_content(prompt)
        return response.text.split('|')
    except:
        return ["Neutral", "Keep moving forward."]

# Weekly Story Helper
def get_weekly_story_text(entries_text):
    model = genai.GenerativeModel('gemini-2.5-flash')
    prompt = f"Here are a user's diary entries for the week: {entries_text}. Write a creative 3rd-person story summarizing their week."
    response = model.generate_content(prompt)
    return response.text

# Image Emotion Helper
def analyze_image_emotion_ai(image_file):
    model = genai.GenerativeModel('gemini-2.5-flash')
    img = Image.open(image_file)
    response = model.generate_content(["Detect the emotion in this image and give a 1 sentence description.", img])
    return response.text