"""Routes for user authentication"""

from datetime import timedelta
from flask import Blueprint, flash, redirect, render_template, request, url_for, abort
from flask_login import current_user, login_user
from sqlalchemy.exc import NoResultFound
from traffic_app import login_manager
from traffic_app.forms import LoginForm, SignupForm
from traffic_app.models import User, db
from urllib.parse import urlparse, urljoin


# Blueprint Configuration
auth_bp = Blueprint("auth_bp", __name__) 

# --------------------------
# User Authentication Routes 
# --------------------------

# Code for login and signup routes are adapted from hackersandslackers tutorial on user authentication with flask login
# Code written by Todd Birchard on harckersandslackers on Apr 4, 2019 is available at: https://hackersandslackers.com/flask-login-user-authentication/

@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    """
    User sign-up page. Register new user (save to database).
    GET requests serve sign-up page.
    POST requests validate form & user creation.
    """
    form = SignupForm()
    if form.validate_on_submit():
        # Check if the email already exists in the database
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash("A user already exists with that email!")
        else:
            # Create a new user via User model
            user = User(
                name=form.name.data, email=form.email.data 
            )
            user.set_password(form.password.data)
            # Create new user record and log the user in
            db.session.add(user)
            db.session.commit()  
            text = f"You are registered! {repr(user)}"
            flash(text)
            login_user(user)  # Log in as newly created user
            return redirect(url_for("main_bp.dashboard"))
    return render_template(
        "signup.html",
        title="Create an Account.",
        form=form,
    )

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Log-in page for registered users.
    Login the user if the password and email are valid.
    GET requests serve Log-in page.
    POST requests validate and redirect user to dashboard.
    """
    # Bypass if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for("main_bp.dashboard"))
    
    form = LoginForm()
    # Validate login attempt
    if form.validate_on_submit():
        try:
            # Query if the user exists, if not raise a NoResultFound error and return to the login form
            user = db.session.execute(
                db.select(User).filter_by(email=form.email.data)
            ).scalar_one()

            if user and user.check_password(form.password.data):
                # If the user exists and their password is correct, login the user
                login_user(
                    user,
                    remember=form.remember.data,
                    duration=timedelta(minutes=1),
                )
                # If they came to login from another page, return them to that page after login, otherwise go to home
                next = request.args.get("next")
                if not is_safe_url(next):
                    return abort(400)
                return redirect(next or url_for("main_bp.dashboard"))
            else:
                flash("Incorrect password")
        except NoResultFound:
            flash("Email address not found")
    return render_template("login.html", title="Login", form=form)


# -------------
# Login Helpers
# -------------

@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in upon page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None

@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash("You must be logged in to view that page.")
    #session['flash'] = True  # Add this line to add flashed message to session
    return redirect(url_for("auth_bp.login"))

def is_safe_url(target):
    """Check if the url is safe for redirection."""
    host_url = urlparse(request.host_url)
    redirect_url = urlparse(urljoin(request.host_url, target))
    return redirect_url.scheme in ('http', 'https') and host_url.netloc == redirect_url.netloc

def get_safe_redirect():
    """Get the redirect url if it is safe."""
    url = request.args.get('next')
    if url and is_safe_url(url):
        return url
    url = request.referrer
    if url and is_safe_url(url):
        return url
    return '/'

