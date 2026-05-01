import datetime
from flask import session
import google.generativeai as genai
from PIL import Image
import io
# Time Travel Helper
def get_current_date():
    if 'simulated_date' in session:
        return datetime.datetime.strptime(session['simulated_date'], "%Y-%m-%d")
    return datetime.datetime.now()

import json
import google.generativeai as genai


def get_ai_emotion_and_motivation(text):
    model = genai.GenerativeModel('gemini-2.5-flash')

    prompt = f"""
    Analyze this diary entry:

    "{text}"

    Choose ONLY ONE emotion from:
    Happy, Sadness, Anger, Fear, Love, Neutral

    Return ONLY JSON:
    {{
        "emotion": "Happy/Sadness/Anger/Fear/Love/Neutral",
        "motivation": "short motivational quote"
    }}
    """

    try:
        response = model.generate_content(prompt)
        output = response.text.strip()

        # 🔥 Clean markdown if Gemini adds ```json
        if output.startswith("```"):
            output = output.replace("```json", "").replace("```", "").strip()

        data = json.loads(output)

        emotion = data.get("emotion", "Neutral")
        motivation = data.get("motivation", "Keep moving forward.")

    except Exception as e:
        print("AI ERROR:", e)
        emotion = "Neutral"
        motivation = "Keep moving forward."

    # ✅ Safety override (VERY IMPORTANT)
    emotion = override_emotion_if_needed(text, emotion)

    return emotion, motivation

def override_emotion_if_needed(text, ai_emotion):
    text = text.lower()

    if ai_emotion == "Neutral":
        if any(w in text for w in ["sad", "cry", "depressed", "lonely"]):
            return "Sadness"
        if any(w in text for w in ["happy", "joy", "excited"]):
            return "Happy"
        if any(w in text for w in ["angry", "mad", "frustrated"]):
            return "Anger"

    return ai_emotion
# Weekly Story Helper
def get_weekly_story_text(entries_text):
    model = genai.GenerativeModel('gemini-2.5-flash')
    prompt = f"Here are a user's diary entries for the week: {entries_text}. Write a creative 3rd-person story summarizing their week."
    response = model.generate_content(prompt)
    return response.text

# Image Emotion Helper

def analyze_image_emotion_ai(image_file):
    model = genai.GenerativeModel('gemini-2.5-flash')

    try:
        # ✅ Read file safely
        image_bytes = image_file.read()
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        response = model.generate_content([
            "Detect the main human emotion in this image in ONE word only.",
            img
        ])

        result = response.text.strip()

        # ✅ Clean output (avoid long sentences)
        return result.split("\n")[0]

    except Exception as e:
        print("IMAGE ERROR:", e)
        return "Error detecting emotion"
    
def get_weekly_advice(emotion_summary):
    model = genai.GenerativeModel('gemini-2.5-flash')

    prompt = f"""
    A user has the following emotional summary for the week:

    {emotion_summary}

    1. Give a short insight about their emotional pattern.
    2. Give practical advice:
       - If negative emotions dominate → suggest how to improve
       - If positive emotions dominate → suggest how to maintain

    Keep it:
    - Short (3-4 lines)
    - Human, supportive tone

    Format:
    Insight: ...
    Advice: ...
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except:
        return "Stay consistent. Take care of your mental well-being."