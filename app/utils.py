import datetime
from flask import session
import google.generativeai as genai
from PIL import Image
import io
import json
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
    Analyze this diary entry carefully.

    Diary Entry:
    "{text}"

    Detect the MOST ACCURATE emotion.

    Choose ONLY ONE emotion from:
    Happy, Sadness, Anger, Fear, Love, Anxiety, Stress, Lonely,
    Excited, Motivated, Confused, Hopeful, Tired, Grateful, Neutral

    Return ONLY valid JSON in this format:
    {{
        "emotion": "emotion_name",
        "motivation": "short motivational quote",
        "suggestions": [
            "suggestion 1",
            "suggestion 2",
            "suggestion 3"
        ]
    }}
    """

    try:
        response = model.generate_content(prompt)
        output = response.text.strip()

        # Remove markdown if Gemini adds ```json
        if output.startswith("```"):
            output = output.replace("```json", "").replace("```", "").strip()

        data = json.loads(output)

        emotion = data.get("emotion", "Neutral")
        motivation = data.get(
            "motivation",
            "Every day is a new beginning."
        )

        suggestions = data.get(
            "suggestions",
            [
                "Take a short break.",
                "Drink some water and relax.",
                "Focus on one small positive step today."
            ]
        )

    except Exception as e:
        print("AI ERROR:", e)

        emotion = "Neutral"

        motivation = "Every day is a new beginning."

        suggestions = [
            "Take a deep breath.",
            "Write down your thoughts.",
            "Do something that makes you smile."
        ]

    # Safety override
    emotion = override_emotion_if_needed(text, emotion)

    return emotion, motivation, suggestions


def override_emotion_if_needed(text, ai_emotion):
    text = text.lower()

    emotion_keywords = {
        "Sadness": [
            "sad", "cry", "depressed", "lonely",
            "hurt", "broken", "upset"
        ],

        "Happy": [
            "happy", "joy", "excited",
            "great", "awesome", "smile"
        ],

        "Anger": [
            "angry", "mad", "frustrated",
            "annoyed", "furious"
        ],

        "Fear": [
            "fear", "scared", "terrified",
            "afraid"
        ],

        "Anxiety": [
            "anxious", "worried", "panic",
            "nervous", "overthinking"
        ],

        "Stress": [
            "stress", "pressure",
            "overwhelmed", "burnout"
        ],

        "Love": [
            "love", "care", "romantic",
            "relationship"
        ],

        "Motivated": [
            "motivated", "determined",
            "focused", "productive"
        ],

        "Tired": [
            "tired", "sleepy",
            "exhausted", "drained"
        ],

        "Hopeful": [
            "hope", "better", "future",
            "improve"
        ],

        "Grateful": [
            "grateful", "thankful",
            "blessed", "appreciate"
        ]
    }

    if ai_emotion == "Neutral":
        for emotion, keywords in emotion_keywords.items():
            if any(word in text for word in keywords):
                return emotion

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