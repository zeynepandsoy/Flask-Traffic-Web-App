from traffic_app.models import User

# -------------------
# Test Database Model
# --------------------

def test_create_new_user():
    """
    GIVEN user information
    WHEN a new User object is created
    THEN check the fields are defined correctly
    """
    # create an instance of the User model class 
    u = User(
        name="John Doe", email="john.doe@example.com"
    )
    # check that its fields are set correctly using set_password() and check_password() methods.
    u.set_password("password123")
    assert u.name == "John Doe"
    assert u.email == "john.doe@example.com"
    assert u.check_password("password123") is True


