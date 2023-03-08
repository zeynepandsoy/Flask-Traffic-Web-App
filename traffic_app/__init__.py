#__init__.py denotes the flask_app folder as a Python package
#The Flask tutorial tells you to create the Flask app object in __init__.py using an application factory function

from flask import Flask


def create_app():
    """Create and configure the Flask app"""
    app = Flask(__name__)

    # Include the routes from routes.py
    with app.app_context():
        from . import routes

    return app

def create_app():
    """
    Initialise the Flask application.
    :rtype: Returns a configured Flask object
    """
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "add_your_key_here"

    # Include the routes from routes.py
    with app.app_context():
        from traffic_app import routes

    return app