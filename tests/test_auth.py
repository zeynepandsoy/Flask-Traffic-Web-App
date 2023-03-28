import pytest
from traffic_app import db
from traffic_app.auth import load_user 
from traffic_app.models import User
#from werkzeug.security import generate_password_hash
from flask_login import current_user
from flask import url_for, flash, get_flashed_messages, request


#check below
def test_valid_login(test_client, authenticated_user):
    """Test that a user can log in with valid credentials"""
    response = test_client.post(
        "/login", 
        data=dict(email=authenticated_user.email, password=authenticated_user.password), #follow_redirects=True,
    )
    response = test_client.get("/", follow_redirects=True)
    assert response.status_code == 200 

    # check that the user is redirected to the dashboard / Assert that the current URL is the main dashboard page URL
    assert request.path == url_for("main_bp.dashboard")

    assert b"Logout" in response.data

    # maybe delete this line
    assert current_user.email == authenticated_user.email


# include variations for this i.e. correct email wrong password vice versa.
def test_invalid_login(test_client):
    """Test that a user cannot log in with invalid credentials"""
    response = test_client.post(
        "/login",
        data=dict(email="wrongemail@test.com", password="wrongpassword"),
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Email address not found" in response.data



# NOT SURE IF THIS IS CORRECT
def test_logout(test_client, authenticated_user):
    """Test that a user can log out"""
    # log in as the user
    test_client.post("/login", data=dict(email=authenticated_user.email, password="password")) #, follow_redirects=True)

    response = test_client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data
    assert b"Signup" in response.data

    # check that the user is no longer authenticated
    assert current_user.is_authenticated == False
    with test_client.session_transaction() as sess:
        assert "user_id" not in sess
    

##  ERROR HANDLIND

def test_login_no_user(test_client):
    """Test that a user cannot log in with an email that does not exist in the database"""
    response = test_client.post(
        "/login",
        data=dict(email="notexist@test.com", password="password"),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Email address not found" in response.data


def test_login_no_password(test_client, new_user):
    """Test that a user cannot log in with no password"""
    response = test_client.post(
        "/login",
        data=dict(email=new_user.email, password=""),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"This field is required" in response.data


def test_login_wrong_password(test_client, new_user):
    """Test that a user cannot log in with the wrong password"""

    response = test_client.post(
        "/login",
        data=dict(email=new_user.email, password="wrongpassword"),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Incorrect password" in response.data



def test_signup_password_mismatch(test_client):
    #Test that a user cannot sign up with a password mismatch
    response = test_client.post('/signup', data={
        'name': 'Another Test User',
        'email': 'anothertestuser@example.com',
        'password': 'password123',
        'confirm': 'password124'
    })

    # Check that the response contains an error message
    assert b'Passwords must match.' in response.data

def test_signup_existing_user(test_client, authenticated_user):
    #Test that a user cannot sign up with an existing email

    # try to sign up with the same email
    response = test_client.post('/signup', data={
        'name': 'Different Test User',
        'email': authenticated_user.email,
        'password': 'testpassword157',
        'confirm': 'testpassword157'
    })
    assert response.status_code == 200
    # check if the error message is present in the response data
    assert b"A user already exists with that email!" in response.data

    # Check that the user was not created with the new credentials
    assert not User.query.filter_by(name='Different Test User').one_or_none()
"""
##FAILS
def test_signup_existing_user(test_client, new_user):
    #Test that a user cannot sign up with an existing email

    # try to sign up with the same email
    response = test_client.post(
        "/signup",
        data=dict(name="testuser3", email=new_user.email, password="testpassword33", confirm_password="testpassword33"),
        follow_redirects=True,
    )

    assert response.status_code == 200
    # check if the error message is present in the response data
    assert b"A user already exists with that email!" in response.data

   # with test_client.session_transaction() as session:
       #assert "A user already exists with that email!" in session['_flashes'][0][1]

    # assert that the user was not actually created with the existing email
    assert not User.query.filter_by(email=new_user.email).one_or_none()
""" 



""" 
def test_login_redirect(test_client, new_user):
    #Test that a user is redirected to the correct page after login
    with test_client.session_transaction() as session:
        session["user_id"] = new_user.id
    response = test_client.get('/', follow_redirects=True)
    # log in as the user
    #response = test_client.post(
       # "/login",
       # data=dict(email=new_user.email, password=new_user.password),
       # follow_redirects=True,
    #)
    assert response.status_code == 200 #SHOUDL THIS BE 200?
    # Check that there was one redirect response.
    assert len(response.history) == 1
    # Check that the second request was to the index page.
    assert response.request.path == "/"

    # check that the user is redirected to the dashboard
    #assert response.request.path == url_for('main_bp.dashboard')
    #assert b"Logout" in response.data
    #assert b"Traffic Home" in response.data


"""
#Test that authorized users are redirected to the home page after login.
def test_login_redirect(authenticated_user, test_client):
    """
    GIVEN a Flask application and an authenticated user (i.e. logged in)
    WHEN the user logs in with valid credentials
    THEN the response redirects to the home page '/'
    """
    # Access the main dashboard page as an authenticated user
    response = test_client.get("/", follow_redirects=True)

    # Assert that the response status code is OK (200) after redirection
    assert response.status_code == 200

    # Assert that the current URL is the main dashboard page URL
    assert request.path == url_for("main_bp.dashboard")

    #assert b"Traffic Home" in response.data
    #assert b"Please choose a category to query traffic volume on:" in response.data

    # Check that we were redirected to the dashboard page
    #assert response.request.path == '/'










# add test to login helper unathorized handles - return you chould be logged in to view that page

## TEST LOGIN HELPER FUNCTIONS 
def test_load_user(test_client, new_user):
    with test_client.application.app_context():
        # test with valid user id
        user = load_user(new_user.id)
        assert user == new_user

        # test with invalid user id
        user = load_user(99999)
        assert user is None

def test_unauthorized_handler(test_client):
    """Test that unauthorized users are redirected to the login page."""
    #try to access an authorised page, similarly this could be response=unauthorized()
    response = test_client.get("/")
    # assert that the response status code is a redirect
    assert response.status_code == 302
    # assert that the response is redirected tp the login page
    assert response.location == url_for("auth_bp.login")

    with test_client.session_transaction() as session:
        assert "You must be logged in to view that page." in session['_flashes'][0][1]

"""
def test_logout(test_client):
    #Test that a user can log out
    response = test_client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"Log In" in response.data
"""
"""
# test_auth_routes.py
testing the functionality of the signup and login routes. The tests are checking if the form is rendered correctly, 
if the form submission is successful, and if the user is redirected to the correct page after submission.

from urllib.parse import urlparse, urljoin
from flask import url_for, request

def test_signup(client, init_database):
    
    GIVEN a Flask application
    WHEN a user submits a sign-up form with valid details
    THEN check if the user is successfully registered and logged in
    
    response = client.get("/signup")
    assert response.status_code == 200

    data = {
        "name": "testuser",
        "email": "testuser@example.com",
        "password": "password",
        "confirm_password": "password",
    }
    response = client.post("/signup", data=data)
    assert response.status_code == 302
    assert urlparse(response.location).path == url_for("main_bp.dashboard")[1:]

def test_login(client, init_database):
    
    GIVEN a Flask application and a registered user
    WHEN the user submits a login form with valid credentials
    THEN check if the user is successfully logged in and redirected to the dashboard
    
    response = client.get("/login")
    assert response.status_code == 200

    data = {
        "email": "user1@example.com",
        "password": "password",
        "remember": False,
    }
    response = client.post("/login", data=data)
    assert response.status_code == 302
    assert urlparse(response.location).path == url_for("main_bp.dashboard")[1:]

"""