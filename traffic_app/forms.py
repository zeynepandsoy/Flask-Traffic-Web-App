"""Sign-up & log-in forms."""

from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, BooleanField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length
)

#put reference

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