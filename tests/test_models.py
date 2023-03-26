from traffic_app.models import User

#create an instance of the model class being tested and check that its fields are set correctly
# Note that for the User model, we also test the set_password() and check_password() methods.
def test_create_new_user():
    """
    GIVEN user information
    WHEN a new User object is created
    THEN check the fields are defined correctly
    """
    u = User(
        name="John Doe", email="john.doe@example.com"
    )
    u.set_password("password123")
    assert u.name == "John Doe"
    assert u.email == "john.doe@example.com"
    assert u.check_password("password123") is True


