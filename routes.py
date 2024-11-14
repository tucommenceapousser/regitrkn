from flask import render_template, redirect, url_for, request, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from models import User, Measurement, ChatHistory, MealPlan
from chat_request import get_coaching_response
import json
from datetime import datetime, timedelta
from flask_wtf.csrf import CSRFError

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
        try:
            username = request.form.get('username')
            password = request.form.get('password')
            
            if not username or not password:
                flash('Veuillez fournir un nom d\'utilisateur et un mot de passe', 'error')
                return render_template('login.html')
            
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password_hash, password):
                login_user(user)
                return redirect(url_for('dashboard'))
            flash('Nom d\'utilisateur ou mot de passe invalide', 'error')
        except CSRFError:
            flash('Échec de la validation du jeton CSRF. Veuillez réessayer.', 'error')
        except Exception as e:
            flash('Une erreur s\'est produite. Veuillez réessayer.', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            
            if not all([username, email, password]):
                flash('Veuillez remplir tous les champs', 'error')
                return render_template('register.html')
            
            if User.query.filter_by(username=username).first():
                flash('Ce nom d\'utilisateur existe déjà', 'error')
                return render_template('register.html')
            
            if User.query.filter_by(email=email).first():
                flash('Cet email est déjà enregistré', 'error')
                return render_template('register.html')
            
            if len(password) < 6:
                flash('Le mot de passe doit contenir au moins 6 caractères', 'error')
                return render_template('register.html')
            
            user = User(
                username=username,
                email=email,
                password_hash=generate_password_hash(password)
            )
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('Inscription réussie!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('Une erreur s\'est produite lors de l\'inscription. Veuillez réessayer.', 'error')
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    measurements = Measurement.query.filter_by(user_id=current_user.id).order_by(Measurement.date.desc()).limit(30).all()
    today_meals = MealPlan.query.filter_by(
        user_id=current_user.id,
        date=datetime.utcnow().date()
    ).order_by(MealPlan.meal_type).all()
    return render_template('dashboard.html', measurements=measurements, meals=today_meals)

@app.route('/add_measurement', methods=['POST'])
@login_required
def add_measurement():
    try:
        measurement = Measurement(
            user_id=current_user.id,
            weight=float(request.form['weight']),
            waist=float(request.form['waist']) if request.form['waist'] else None,
            body_fat=float(request.form['body_fat']) if request.form['body_fat'] else None,
            notes=request.form['notes']
        )
        db.session.add(measurement)
        db.session.commit()
        flash('Mesure ajoutée avec succès!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Erreur lors de l\'ajout de la mesure. Veuillez réessayer.', 'error')
    return redirect(url_for('dashboard'))

@app.route('/meal_plan', methods=['GET'])
@login_required
def meal_plan():
    # Get meals for the last 7 days
    start_date = datetime.utcnow() - timedelta(days=7)
    meals = MealPlan.query.filter(
        MealPlan.user_id == current_user.id,
        MealPlan.date >= start_date
    ).order_by(MealPlan.date.desc(), MealPlan.meal_type).all()
    return render_template('meal_plan.html', meals=meals)

@app.route('/add_meal', methods=['POST'])
@login_required
def add_meal():
    try:
        meal = MealPlan(
            user_id=current_user.id,
            meal_type=request.form['meal_type'],
            name=request.form['name'],
            description=request.form['description'],
            calories=int(request.form['calories']) if request.form['calories'] else None,
            protein=float(request.form['protein']) if request.form['protein'] else None,
            carbs=float(request.form['carbs']) if request.form['carbs'] else None,
            fats=float(request.form['fats']) if request.form['fats'] else None
        )
        db.session.add(meal)
        db.session.commit()
        flash('Repas ajouté avec succès!', 'success')
        return jsonify({'status': 'success', 'message': 'Repas ajouté avec succès!'})
    except Exception as e:
        db.session.rollback()
        flash('Erreur lors de l\'ajout du repas. Veuillez réessayer.', 'error')
        return jsonify({'status': 'error', 'message': 'Erreur lors de l\'ajout du repas.'}), 400

@app.route('/get_meal_suggestions', methods=['POST'])
@login_required
def get_meal_suggestions():
    try:
        message = "Veuillez suggérer un plan de repas sain basé sur mes objectifs de perte de poids."
        latest_measurement = Measurement.query.filter_by(user_id=current_user.id).order_by(Measurement.date.desc()).first()
        
        user_context = {
            'weight': latest_measurement.weight if latest_measurement else 'unknown',
            'progress': 'maintaining' if not latest_measurement else 'unknown',
            'request_type': 'meal_plan',
            'language': 'fr'
        }
        
        response = get_coaching_response(message, user_context)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'response': 'Une erreur s\'est produite. Veuillez réessayer.'}), 500

@app.route('/chat')
@login_required
def chat():
    chat_history = ChatHistory.query.filter_by(user_id=current_user.id).order_by(ChatHistory.timestamp.desc()).limit(10).all()
    return render_template('chat.html', chat_history=chat_history)

@app.route('/get_advice', methods=['POST'])
@login_required
def get_advice():
    try:
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
    except CSRFError:
        return jsonify({'response': 'CSRF token validation failed. Please refresh the page and try again.'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'response': 'An error occurred. Please try again.'}), 500

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Vous avez été déconnecté avec succès.', 'info')
    return redirect(url_for('login'))

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    flash('Échec de la validation du jeton CSRF. Veuillez réessayer.', 'error')
    return redirect(url_for('login'))