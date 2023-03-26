"""Initialize app."""

from pathlib import Path
from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_marshmallow import Marshmallow

# Sets the project root folder
PROJECT_ROOT = Path(__file__).parent.joinpath('traffic_app')

# Create a global SQLAlchemy object
db = SQLAlchemy()
# Create a global LoginManager object
login_manager = LoginManager()
# Create a global Flask-Marshmallow object
ma = Marshmallow()

# Application Factory Function
def create_app(config_object): 
    """Create and configure the Flask app"""
    #Initialise the Flask application.
    app = Flask(__name__)
    # Application Configuration, see config parameters in config.py
    app.config.from_object(config_object) 
    
    #login_manager.login_view = 'auth_bp.login' should be added 
    
    # Initialise extensions
    initialize_extensions(app)

    with app.app_context():
        from . import routes, auth

        # Register Blueprints
        app.register_blueprint(routes.main_bp)
        app.register_blueprint(auth.auth_bp)

        # Create Database Models
        db.create_all()

        return app
    
def initialize_extensions(app):
    """Binds extensions to the Flask application instance (app)"""
    db.init_app(app)
    login_manager.init_app(app)
    ma.init_app(app)


# Included imports at the end to prevent circular imports 
from .models import User, Query
#from .schemas import UserSchema, QuerySchema