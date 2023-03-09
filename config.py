
"""Flask configuration."""
from pathlib import Path

# Sets the project root folder
PROJECT_ROOT = Path(__file__).parent

class Config:
    """Set Flask configuration from environment variables."""

    #FLASK_APP=wsgi.py
    FLASK_ENV = "production"
    SECRET_KEY = "cQw2uTRiHEXGWVAepfDAqg"
    #SQLALCHEMY_DATABASE_URI=mysql+pymysql://myuser:mypassword@host.example.com:1234/mydatabase
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + str(PROJECT_ROOT.joinpath("data", "traffic.db"))
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"




