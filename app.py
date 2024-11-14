import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# create the app
app = Flask(__name__)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Setup secret key for sessions
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "trkntrkn"

# Initialize the app with the extension
db.init_app(app)

with app.app_context():
    # Import routes after db initialization to avoid circular imports
    from routes import *  # noqa: F403
    
    # Import models and create all tables
    import models  # noqa: F401
    db.create_all()

# Register error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

# Enable CSRF protection
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)
