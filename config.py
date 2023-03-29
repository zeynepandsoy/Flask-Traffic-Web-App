
from pathlib import Path

# --------------------
# Flask Configuration
# --------------------

# Sets the project root folder
PROJECT_ROOT = Path(__file__).parent.joinpath('traffic_app')

class Config:
    """Base config."""

    SECRET_KEY = "cQw2uTRiHEXGWVAepfDAqg"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + str(
        PROJECT_ROOT.joinpath("data", "traffic.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


class ProdConfig(Config):
    """Production config.
    Not currently implemented.
    """

    pass


class DevConfig(Config):
    """Development config"""

    FLASK_ENV = "development"
    DEBUG = True
    TESTING = True


class TestConfig(Config):
    """Testing config"""

    TESTING = True
    SQLALCHEMY_ECHO = True
    WTF_CSRF_ENABLED = False
    #SERVER_NAME = "127.0.0.1:5000"  

