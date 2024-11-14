from flask import render_template, redirect, url_for, request, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from models import User, Measurement, ChatHistory
from chat_request import get_coaching_response
import json
from datetime import datetime, timedelta

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
@login_required
def index():
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password_hash, request.form['password']):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if User.query.filter_by(username=request.form['username']).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        
        user = User(
            username=request.form['username'],
            email=request.form['email'],
            password_hash=generate_password_hash(request.form['password'])
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('dashboard'))
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    measurements = Measurement.query.filter_by(user_id=current_user.id).order_by(Measurement.date.desc()).limit(30).all()
    return render_template('dashboard.html', measurements=measurements)

@app.route('/add_measurement', methods=['POST'])
@login_required
def add_measurement():
    measurement = Measurement(
        user_id=current_user.id,
        weight=float(request.form['weight']),
        waist=float(request.form['waist']) if request.form['waist'] else None,
        body_fat=float(request.form['body_fat']) if request.form['body_fat'] else None,
        notes=request.form['notes']
    )
    db.session.add(measurement)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/chat')
@login_required
def chat():
    chat_history = ChatHistory.query.filter_by(user_id=current_user.id).order_by(ChatHistory.timestamp.desc()).limit(10).all()
    return render_template('chat.html', chat_history=chat_history)

@app.route('/get_advice', methods=['POST'])
@login_required
def get_advice():
    message = request.form['message']
    latest_measurement = Measurement.query.filter_by(user_id=current_user.id).order_by(Measurement.date.desc()).first()
    
    user_context = {
        'weight': latest_measurement.weight if latest_measurement else 'unknown',
        'progress': 'maintaining' if not latest_measurement else 'unknown'
    }
    
    response = get_coaching_response(message, user_context)
    
    chat_entry = ChatHistory(
        user_id=current_user.id,
        message=message,
        response=response
    )
    db.session.add(chat_entry)
    db.session.commit()
    
    return jsonify({'response': response})

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
