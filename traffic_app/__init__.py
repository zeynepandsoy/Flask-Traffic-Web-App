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

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    """Construct the core app object."""
    app = Flask(__name__, instance_relative_config=False)

    # Application Configuration
    app.config.from_object('config.Config')

    # Initialize Plugins
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from traffic_app import routes
        from traffic_app import auth
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