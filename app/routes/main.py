from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from bson.objectid import ObjectId
import datetime  # <--- THIS WAS MISSING
from app.extensions import mongo
from app.utils import get_current_date, get_ai_emotion_and_motivation
from app.utils import get_weekly_advice
import json
main_bp = Blueprint('main', __name__)

@main_bp.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    current_date = get_current_date()

    user_id = session['user_id']

    # Start + End of current day
    start_of_day = datetime.datetime(
        current_date.year,
        current_date.month,
        current_date.day
    )

    end_of_day = start_of_day + datetime.timedelta(days=1)

    # Get today's entry
    today_entry = mongo.db.entries.find_one({
        'user_id': user_id,
        'date': {
            '$gte': start_of_day,
            '$lt': end_of_day
        }
    })

    # Decode suggestions JSON
    if today_entry and 'suggestions' in today_entry:

        try:
            today_entry['suggestions'] = json.loads(
                today_entry['suggestions']
            )

        except:
            today_entry['suggestions'] = []

    # Get all entries
    entries = list(
        mongo.db.entries.find({
            'user_id': user_id
        }).sort('date', -1)
    )

    # Decode suggestions for all entries too
    for entry in entries:

        if 'suggestions' in entry:

            try:
                entry['suggestions'] = json.loads(
                    entry['suggestions']
                )

            except:
                entry['suggestions'] = []

    return render_template(
        'dashboard.html',
        entries=entries,
        current_date=current_date,
        today_entry=today_entry
    )
@main_bp.route('/write', methods=['GET', 'POST'])
def write():
    if 'user_id' not in session: return redirect(url_for('auth.login'))
    
    # 1. GET THE CURRENT DATE (Real or Time-Travelled)
    current_date = get_current_date() 

    if request.method == 'POST':
        content = request.form['content']
        emotion, motivation, suggestions = get_ai_emotion_and_motivation(content)
        
        entry = {
            'user_id': session['user_id'],
            'content': content,
            'date': current_date, # Use the date variable
            'emotion': emotion.strip(),
            'motivation': motivation.strip(),
            'suggestions':json.dumps(suggestions),
            'type': 'text'
        }
        mongo.db.entries.insert_one(entry)
        return redirect(url_for('main.dashboard'))
    
    # 2. PASS 'current_date' TO THE TEMPLATE HERE
    return render_template('write.html', current_date=current_date)

@main_bp.route('/chat')
def chat():
    if 'user_id' not in session: return redirect(url_for('auth.login'))
    return render_template('chat.html')

@main_bp.route('/edit/<entry_id>', methods=['POST'])
def edit_entry(entry_id):
    if 'user_id' not in session: return redirect(url_for('auth.login'))
    
    entry = mongo.db.entries.find_one({'_id': ObjectId(entry_id)})
    current_date = get_current_date()
    
    # Calculate the difference between now and the entry date
    delta = current_date - entry['date']
    
    # Check if less than 2 days have passed
    if delta.days < 2:
        new_content = request.form['content']
        mongo.db.entries.update_one({'_id': ObjectId(entry_id)}, {'$set': {'content': new_content}})
        flash('Entry updated.')
    else:
        flash('This entry is too old to edit.')
        
    return redirect(url_for('main.dashboard'))


@main_bp.route('/weekly_emotions')
def weekly_emotions():
    if 'user_id' not in session:
        return {"error": "Unauthorized"}, 401

    user_id = session['user_id']
    offset = int(request.args.get('offset', 0))

    today = get_current_date()

    start_of_week = today - datetime.timedelta(days=today.weekday())
    start_of_week += datetime.timedelta(weeks=offset)

    start_datetime = datetime.datetime(
        start_of_week.year,
        start_of_week.month,
        start_of_week.day
    )

    end_datetime = start_datetime + datetime.timedelta(days=7)

    entries = list(mongo.db.entries.find({
        'user_id': user_id,
        'date': {'$gte': start_datetime, '$lt': end_datetime}
    }))

    emotion_count = {}

    for e in entries:
        emotion = e.get('emotion', 'Unknown').strip().capitalize()
        emotion_count[emotion] = emotion_count.get(emotion, 0) + 1

    # 🔥 Generate advice
    advice = get_weekly_advice(emotion_count)

    return {
        "week_start": start_datetime.strftime('%Y-%m-%d'),
        "week_end": (end_datetime - datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
        "emotions": emotion_count,
        "advice": advice
    }