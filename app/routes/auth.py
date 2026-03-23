from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.extensions import mongo, bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET', 'POST']) # Root redirects to login
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'username': request.form['username']})
        if login_user and bcrypt.check_password_hash(login_user['password'], request.form['password']):
            session['user_id'] = str(login_user['_id'])
            session['username'] = login_user['username']
            return redirect(url_for('main.dashboard'))
        flash('Invalid username or password')
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'username': request.form['username']})
        if existing_user:
            flash('Username already exists!')
            return redirect(url_for('auth.register'))
        
        hashed_password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        users.insert_one({'username': request.form['username'], 'password': hashed_password})
        flash('Account created! Please login.')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))