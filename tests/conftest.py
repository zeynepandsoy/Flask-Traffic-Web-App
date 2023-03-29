
import pytest
from traffic_app import db, create_app 
from config import TestConfig
from traffic_app.models import User


# ------------------------------
# Fixtures for Flask route tests
# ------------------------------


@pytest.fixture(scope="session")
def app():
    """Create a Flask app configured for testing"""
    # factory function that creates and configures the Flask app
    app = create_app(TestConfig) 
    yield app


# test_client fixture simulates HTTP requests and checks the responses
# authenticated_user fixture creates a test user and logs them in before running the tests

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
    yield user 
    # cleanup after the test
    db.session.delete(user)
    db.session.commit()


@pytest.fixture(scope="function")
def authenticated_user(test_client): 
    """Fixture that logs in a test user"""
    # Create a test user
    user = User(name="auth user", email="auth_user@example.com")
    user.set_password("password")
    db.session.add(user)
    db.session.commit()

    # Log in the user
    test_client.post("/login", data=dict(email=user.email, password="password"))
    yield user 
    # cleanup after the test
    db.session.delete(user)
    db.session.commit()

"""
Instead of below fixture, its functionality is implemented seperately on each fixture defined above
@pytest.fixture(scope="function", autouse=True)
def clean_db():
    # Rolls back the database session and deletes any users created during the tests to keep the database clean
    yield
    db.session.rollback()
    db.session.query(User).delete()
    db.session.commit()
"""
