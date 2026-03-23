from flask import Blueprint, request, jsonify, session, redirect, url_for, flash
import google.generativeai as genai
import datetime
from app.extensions import mongo
from app.utils import get_current_date, get_weekly_story_text, analyze_image_emotion_ai
from bson import json_util # You might need this, or just use str()
import json


api_bp = Blueprint('api', __name__)

@api_bp.route('/generate_weekly_story')
def generate_weekly_story_route():
    if 'user_id' not in session: return jsonify({'error': 'auth'})
    
    current_date = get_current_date()
    one_week_ago = current_date - datetime.timedelta(days=7)
    
    entries = mongo.db.entries.find({
        'user_id': session['user_id'],
        'date': {'$gte': one_week_ago, '$lte': current_date}
    })
    
    text_blob = " ".join([e['content'] for e in entries])
    if not text_blob: return jsonify({'story': "Not enough entries this week!"})
    
    story = get_weekly_story_text(text_blob)
    return jsonify({'story': story})

@api_bp.route('/analyze_photo', methods=['POST'])
def analyze_photo_route():
    if 'photo' not in request.files: return jsonify({'error': 'No file'})
    file = request.files['photo']
    result = analyze_image_emotion_ai(file)
    return jsonify({'result': result})

@api_bp.route('/chat_assistant', methods=['POST'])
def chat_assistant():
    data = request.json
    user_msg = data.get('message')
    model = genai.GenerativeModel('gemini-2.5-flash')
    chat = model.start_chat(history=[])
    response = chat.send_message(user_msg)
    return jsonify({'reply': response.text})

@api_bp.route('/get_entry/<date_str>')
def get_entry(date_str):
    if 'user_id' not in session: return jsonify({'error': 'auth'})
    
    # Parse the date string to a datetime object
    try:
        query_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return jsonify({'error': 'Invalid date format'})

    # Find entry for this specific day (ignoring time)
    # We use a range to cover the whole 24 hours of that day
    next_day = query_date + datetime.timedelta(days=1)
    
    entry = mongo.db.entries.find_one({
        'user_id': session['user_id'],
        'date': {'$gte': query_date, '$lt': next_day}
    })
    
    if entry:
        # Check if editable (2 day rule)
        # Note: We use the *simulated* current date for the rule check
        simulated_now = get_current_date()
        is_locked = (simulated_now - entry['date']).days >= 2

        return jsonify({
            'found': True,
            'content': entry['content'],
            'emotion': entry.get('emotion', 'Neutral'),
            'motivation': entry.get('motivation', ''),
            'is_locked': is_locked
        })
    else:
        return jsonify({'found': False})

@api_bp.route('/set_time', methods=['POST'])
def set_time():
    date_str = request.form['date']
    session['simulated_date'] = date_str
    flash(f"🕒 Time Travelled to {date_str}")
    return redirect(url_for('main.dashboard'))