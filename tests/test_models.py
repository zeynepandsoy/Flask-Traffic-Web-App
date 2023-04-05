from traffic_app.models import User, Query

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


def test_query_model():
    """
    GIVEN query information
    WHEN a new Query object is created
    THEN check the fields are defined correctly
    """
    # create an instance of the Query model class
    query = Query(holiday='Independence Day', weather='Clear', traffic_volume=3214, year=2015, month=3, day=16, hour=10, categorized_hour='Afternoon', categorized_weekday='Sunday')
    
    # check that its fields are set correctly
    assert query.holiday == 'Independence Day'
    assert query.weather == 'Clear'
    assert query.traffic_volume == 3214
    assert query.year == 2015
    assert query.month == 3
    assert query.day == 16
    assert query.hour == 10
    assert query.categorized_hour == 'Afternoon'
    assert query.categorized_weekday == 'Sunday'

    # check that the __repr__ method returns a string with the correct format
    assert str(query) == "<Query: Independence Day,Clear, 3214, 2015,3,16, 10, Afternoon,Sunday>"

