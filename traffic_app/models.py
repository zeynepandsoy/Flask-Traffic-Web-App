"""Database models."""

from traffic_app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# ---------------
# Database Models
# ---------------

class User(UserMixin, db.Model):
    """User account model."""

    __tablename__ = 'flasklogin-users'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(100),
        nullable=False,
        unique=False
    )
    email = db.Column(
        db.String(40),
        unique=True,
        nullable=False
    )
    password = db.Column(
        db.String(200),
        primary_key=False,
        unique=False,
        nullable=False
	)
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(
            password,
            method='sha256'
        )    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.name)
    

class Query(db.Model):
    """Model for Traffic Query Parameters"""

    __tablename__ = "newdatabase"
    rowid = db.Column(db.Integer, primary_key=True)
    holiday = db.Column(db.Text, nullable=False)
    weather = db.Column(db.Text, nullable=False)
    traffic_volume = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    day = db.Column(db.Integer, nullable=False)
    hour = db.Column(db.Integer, nullable=False)
    categorized_hour = db.Column(db.Text, nullable=False)
    categorized_weekday = db.Column(db.Text, nullable=False)


    def __init__(self, holiday, weather, traffic_volume, year, month, day, hour, categorized_hour, categorized_weekday):
        self.holiday = holiday
        self.weather = weather
        self.traffic_volume = traffic_volume
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.categorized_hour = categorized_hour 
        self.categorized_weekday = categorized_weekday 


    def __repr__(self):
        """
        Returns the attributes of query as a string
        :returns str
        """
        clsname = self.__class__.__name__
        return f"<{clsname}: {self.holiday},{self.weather}, {self.traffic_volume}, {self.year},{self.month},{self.day}, {self.hour}, {self.categorized_hour},{self.categorized_weekday}>" 



