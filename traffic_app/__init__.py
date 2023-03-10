#__init__.py denotes the flask_app folder as a Python package
#The Flask tutorial tells you to create the Flask app object in __init__.py using an application factory function
"""
from flask import Flask

def create_app():
    
    #Initialise the Flask application.
    #:rtype: Returns a configured Flask object
    
    app = Flask(__name__)
    #app.config["SECRET_KEY"] = "cQw2uTRiHEXGWVAepfDAqg"

    # Include the routes from routes.py
    with app.app_context():
        from traffic_app import routes

    return app
"""
"""Initialize app."""

from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Sets the project root folder
PROJECT_ROOT = Path(__file__).parent.joinpath('traffic_app')

# Create a global SQLAlchemy object
db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_object): #config_class
    """Create and configure the Flask app"""
    app = Flask(__name__) #, instance_relative_config=False

    # Application Configuration, See config parameters in config.py
    app.config.from_object(config_object) #config_class   'config.Config'
    
    """
    # Initialize Plugins
    db.init_app(app)
    login_manager.init_app(app)
    """
    # Uses a helper function to initialise extensions
    initialize_extensions(app)

    with app.app_context():
        from traffic_app import routes, auth
        #from traffic_app.models import User
        #from .assets import compile_assets

        # Register Blueprints
        app.register_blueprint(routes.main_bp)
        app.register_blueprint(auth.auth_bp)

        # Create Database Models
        db.create_all()

        # Compile static assets
        #if app.config['FLASK_ENV'] == 'development':
        #    compile_assets(app)

        return app
    
def initialize_extensions(app):
    """Binds extensions to the Flask application instance (app)"""
    # Flask-SQLAlchemy
    db.init_app(app)
    # login manager
    login_manager.init_app(app)