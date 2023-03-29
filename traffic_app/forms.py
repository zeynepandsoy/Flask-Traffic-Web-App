"""Sign-up & log-in forms."""

from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, BooleanField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length
)

# --------------------
# Authentication Forms 
# --------------------

# Code for SignupForm and LoginForm routes are adapted from hackersandslackers tutorial on user authentication with flask login
# Code written by Todd Birchard on harckersandslackers on Apr 4, 2019 is available at: https://hackersandslackers.com/flask-login-user-authentication/


class SignupForm(FlaskForm):
    """User Sign-up Form."""
    name = StringField(
        'Name',
        validators=[DataRequired()]
    )
    email = EmailField(
        'Email',
        validators=[
            Length(min=6),
            Email(message='Enter a valid email.'),
            DataRequired()
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=6, message='Select a stronger password.')
        ]
    )
    confirm = PasswordField(
        'Confirm Your Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    """User Log-in Form."""
    email = EmailField(label='Email address', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember = BooleanField(label='Remember me')
    submit = SubmitField(label='Log In')

    """
    HANDLED ELSEWHERE
    def validate_email(self, email):
    	user = User.query.filter_by(email=email.data).first()
    	if user is None:
        	raise ValidationError('No account found with that email address.')

	def validate_password(self, password):
    	user = User.query.filter_by(email=self.email.data).first()
    	if user is None:
        	raise ValidationError('No account found with that email address.')
    	if not user.check_password(password.data):
        	raise ValidationError('Incorrect password.')
    """