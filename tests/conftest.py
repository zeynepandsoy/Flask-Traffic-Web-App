import pytest
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
from flask import url_for

from traffic_app import db, create_app #, config
from config import TestConfig
from traffic_app.models import User, Query
from werkzeug.security import generate_password_hash




"""
@pytest.fixture(scope="session")
def app():
    #Create a Flask app configured for testing
    app = create_app(config.TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()
"""

# Used for Flask route tests and Selenium tests
@pytest.fixture(scope="session")
def app():
    """Create a Flask app configured for testing"""
    app = create_app(TestConfig) #config.TestConfig)
    yield app

# Used for Flask route tests
@pytest.fixture(scope="function")
def test_client(app):
    """Create a Flask test client"""
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client



@pytest.fixture(scope='function')
def new_user():
    """Create a new user for testing"""
    user = User(name="Test User", email="testuser@test.com", password="testpassword")
    db.session.add(user)
    db.session.commit()
    yield user #should this be return user and delete below?
    # cleanup after the test
    db.session.delete(user)
    db.session.commit()


@pytest.fixture(scope="function")
def authenticated_user(test_client): #db
    """Fixture that logs in a test user"""
    # Create a test user
    user = User(name="auth user", email="auth_user@example.com")
    user.set_password("password")
    db.session.add(user)
    db.session.commit()

    # Log in the user
    test_client.post("/login", data=dict(email=user.email, password="password"))

    yield user #return user and delete below?
    # cleanup after the test
    db.session.delete(user)
    db.session.commit()

"""
#rolls back the database session and deletes any users created during the tests to keep the database clean
@pytest.fixture(scope="function", autouse=True)
def clean_db():
    #Fixture that cleans up the database after each test
    yield
    db.session.rollback()
    db.session.query(User).delete()
    db.session.commit()
"""
"""
@pytest.fixture(scope="function")
def authenticated_user(test_client):
    #Fixture that logs in a test user
    # Create a test user
    user = User(name="test_user", email="test_user@example.com")
    user.set_password("password")
    db.session.add(user)
    db.session.commit()

    # Log in the user
    response = test_client.post(
        url_for('auth_bp.login'),
        data=dict(email='test_user@example.com', password='password'),
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"You are now logged in!" in response.data

    return user
"""
"""
# Used for Selenium tests
@pytest.fixture(scope="session")
def chrome_driver():
    #Selenium webdriver with options to support running in GitHub actions
    #Note:
        #For CI: `headless` not commented out
        #For running on your computer: `headless` to be commented out
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    driver = Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()
"""








""" 
incorporate the following code for my case
# Used for Selenium tests ?

# Data for any tests
@pytest.fixture(scope="module")
def region_json():
    #Creates a new region JSON for tests
    reg_json = {
        "NOC": "NEW",
        "region": "New Region",
        "notes": "Some notes about the new region",
    }
    return reg_json


# Data for any tests
@pytest.fixture(scope="module")
def region():
    #Creates a new region object for tests
    new_region = Region(
        NOC="NEW", region="New Region", notes="Some notes about the new region"
    )
    return new_region

"""