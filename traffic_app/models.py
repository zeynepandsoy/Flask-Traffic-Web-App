"""Database models."""
from traffic_app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash



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
        return '<User {}>'.format(self.username)
    
# INCLUDE MODELS FOR TRAFFIC APP, make 1st page like paralympics event page, link to dashboard.html
#also serialize the data 
#i.e.:
"""
class Query(db.Model):
    'Traffic observation parameters/queries'

    __tablename__ = "query"
    observation_id = db.Column(db.Integer, primary_key=True)
    weather = db.Column(db.Text, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    ...
"""

class Query(db.Model):
    """Traffic Query Parameters"""

    __tablename__ = "query"
    record_id = db.Column(db.Integer, primary_key=True)
    holiday = db.Column(db.Text, nullable=False)
    weather = db.Column(db.Text, nullable=False)
    traffic_volume = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    day = db.Column(db.Integer, nullable=False)
    hour = db.Column(db.Integer, nullable=False)
    categorized_hour = db.Column(db.Text, nullable=False)
    categorized_weekday = db.Column(db.Text, nullable=False)

    def __repr__(self):
        """
        Returns the attributes of the event as a string
        :returns str
        """
        clsname = self.__class__.__name__
        return f"<{clsname}: {self.holiday},{self.weather}, {self.traffic_volume}, {self.year},{self.month},{self.day}, {self.hour}, {self.categorized_hour},{self.categorized_weekday}>" 

    
"""
define a Class:
def for column(weather) in Query.columns
print unique.values(cloud, sunny ...) of chosen column (dropdown)
    for chosen unique.value() of chosen column
    return
    get_max(traffic volume)
    get_min(traffic volume)
    get_avg(traffic volume)
    string representattion:
    f'string("average traffic volume of {{...}} is {{relatively high/low, quite average}}")

"""
