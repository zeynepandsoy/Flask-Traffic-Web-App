
from traffic_app.auth import load_user
from traffic_app.models import User
from flask_login import current_user
from flask import url_for, request

# --------------------------
# Test Authentication Routes
# --------------------------

def test_valid_login(test_client, authenticated_user):
    """
    GIVEN an authenticated user 
    WHEN the user attempts to login with valid login credentials
    THEN the user is able to login successfully
      and the user is redirected to the main page
    """
    # login with valid credentials
    response = test_client.post(
        "/login", 
        data=dict(email=authenticated_user.email, password=authenticated_user.password)
    )
    response = test_client.get("/", follow_redirects=True)

    # check if the response status was successful 
    assert response.status_code == 200 

    # check that the user is redirected to the main dashboard page
    assert request.path == url_for("main_bp.dashboard")

    # check that the logout link is present in the response data
    assert b"Logout" in response.data

    # check that the email of the current user matches the authenticated user email
    assert current_user.email == authenticated_user.email


def test_invalid_login(test_client):
    """
    GIVEN an authenticated user 
    WHEN the user attempts to login with invalid login credentials
    THEN the user is not able to login  
        and is shown an error message 'Email address not found'
    """
    # attempt to login with invalid credentials  
    response = test_client.post(
        "/login",
        data=dict(email="wrongemail@test.com", password="wrongpassword"),
        follow_redirects=True,
    )
    # check that the user is not authenticated
    assert current_user.is_authenticated == False

    # check if the user received an error message 'Email address not found'
    assert b"Email address not found" in response.data


def test_logout(test_client, authenticated_user):
    """
    GIVEN a user who is authenticated and logged in
    WHEN the user attempts to logs out
    THEN the user is able to log out successfully,
        and the 'Login' and 'Signup' buttons are present in the response data.
    """
    # log in as the user
    test_client.post("/login", data=dict(email=authenticated_user.email, password="password")) #, follow_redirects=True)
    
    # log out as the user
    response = test_client.get("/logout", follow_redirects=True)

    assert response.status_code == 200
    # check that the response data contains the 'Login' and 'Signup' buttons
    assert b"Login" in response.data
    assert b"Signup" in response.data
    # check that the user is no longer authenticated
    assert current_user.is_authenticated == False
    # further check that the user_id is not present in the session
    with test_client.session_transaction() as sess:
        assert "user_id" not in sess
    

def test_valid_signup(test_client):
    """ 
    GIVEN a user who is not authenticated
    WHEN the user attempts to sign up with valid credentials
    THEN the user is able to sign up successfully,
        and is redirected to the main page,
    """
    # sign up as a new user
    response = test_client.post('/signup', data={
        'name': 'Valid Test User',
        'email': 'validtestuser@example.com',
        'password': 'validpassword',
        'confirm': 'validpassword'
    }, follow_redirects=True)

    # log in as the new user 
    response = test_client.post("/login", data=dict(email='validtestuser@example.com', password="validpassword"), follow_redirects=True)

    # check that the response status code after the redirect was 200 (OK)
    assert response.status_code == 200

    # check that the response is redirected to the main page
    assert response.request.path == "/" 

    # check that the user is authenticated
    assert current_user.is_authenticated == True

    #assert b'You are registered!' in response.data
    assert b'Traffic Home' in response.data


# Test that cover Error Handling
# ------------------------------

def test_login_no_user(test_client, new_user):
    """
    GIVEN an authenticated new user 
    WHEN the user attempts to login with an email that does not exist in the database
    THEN the user is not able to login
        and is shown an error message 'Email address not found'
    """
    # try to log in with an email that does not exist in the database
    response = test_client.post(
        "/login",
        data=dict(email="notexist@test.com", password=new_user.password),
        follow_redirects=True,
    )
    #assert response.status_code == 200
    # check if error message is present in the response data
    assert b"Email address not found" in response.data


def test_login_no_password(test_client, new_user):
    """
    GIVEN an authentiated new user 
    WHEN the user attempts to login with blank password
    THEN the user is not able to login
        and is shown an error message 'This field is required'
    """
    #try to log in with no password
    response = test_client.post(
        "/login",
        data=dict(email=new_user.email, password=""),
        follow_redirects=True,
    )
    assert response.status_code == 200
    # check if error message is present in the response data
    assert b"This field is required" in response.data


def test_login_wrong_password(test_client, new_user):
    """
    Test that a user cannot log in with the wrong password
    GIVEN an authenticated new user 
    WHEN the user attempts to login with the wrong password
    THEN the user is not able to login
        and is shown an error message 'Incorrect password'
    """
    # try to log in with the wrong password
    response = test_client.post(
        "/login",
        data=dict(email=new_user.email, password="wrongpassword"),
        follow_redirects=True,
    )
    assert response.status_code == 200
    # check if error message is present in the response data
    assert b"Incorrect password" in response.data



def test_signup_password_mismatch(test_client):
    """
    GIVEN a user who is not authenticated
    WHEN the user attempts to sign up with a password mismatch, i.e. password != confirm
    THEN the user is not able to sign up
        and is shown an error message 'Passwords must match.'
    """
    # try to sign up with a password mismatch
    response = test_client.post('/signup', data={
        'name': 'Another Test User',
        'email': 'anothertestuser@example.com',
        'password': 'password123',
        'confirm': 'password124'
    })

    # Check if error message is present in the response data
    assert b'Passwords must match.' in response.data


def test_signup_existing_user(test_client, authenticated_user):
    """
    GIVEN a user who is not authenticated
    WHEN the user attempts to sign up with an already existing email
    THEN the user is not able to sign up
        and is shown an error message 'A user already exists with that email!'
    """

    # try to sign up with an already existing email
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
    

def test_login_redirect(test_client, authenticated_user):
    """
    Test that authorized users are redirected to the home page after login.
    GIVEN an authenticated user
    WHEN the user logs in with valid credentials
    THEN the response redirects to the home page '/'
    """
    # Log in as the user
    response = test_client.post("/login", data=dict(email=authenticated_user.email, password="password"), follow_redirects=True) 

    # Check that the response status code is 200 OK.
    assert response.status_code == 200  

    # Check that there was one redirect response.
    assert len(response.history) == 1

    # Check that the user is redirected to the main page.
    assert response.request.path == "/" #url_for("main_bp.dashboard")

    # Check that Logout and Traffic Home are present in the response data.
    assert b"Logout" in response.data
    assert b"Traffic Home" in response.data


# Tests for Login Helper Functions
# --------------------------------


def test_load_user(test_client, new_user):
    """
    GIVEN a new user with a valid user ID and an invalid user ID
    WHEN the load_user function is called with the user ID
    THEN the corresponding user object is returned only if user ID is valid, otherwise return None
    """
    with test_client.application.app_context():
        # test with valid user id
        user = load_user(new_user.id)
        # check that the user object returned is the same as the new user object
        assert user == new_user

        # test with invalid user id
        user = load_user(99999)
        # check that the user object returned is None
        assert user is None


def test_unauthorized_handler(test_client):
    """
    GIVEN a user who is not authenticated
    WHEN the user attempts to access an authorised page
    THEN the user is redirected to the login page
        and is shown an error message 'You must be logged in to view that page.'
    """
    # try to access an authorised page
    response = test_client.get("/")  #response=unauthorized()
    # check that the response status code is a redirect
    assert response.status_code == 302
    # check that the response is redirected tp the login page
    assert response.location == url_for("auth_bp.login")

    # check that the error message 'You must be logged in to view that page.' is flashed
    with test_client.session_transaction() as session:
        assert "You must be logged in to view that page." in session['_flashes'][0][1]
