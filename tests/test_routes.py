
from traffic_app.models import Query
"""
using the test_client fixture to simulate HTTP requests and check the responses. 
using the authenticated_user fixture to create a test user and log them in before running the tests.
"""

def test_dashboard(test_client, authenticated_user): 
    """
    Test dashboard page is accessible when logged in
    GIVEN the user is logged in
    WHEN the user requests the dashboard page
    THEN the page should load successfully and display the correct content
    """
    # Log in the user using the authenticated_user fixture
    user = authenticated_user

    response = test_client.get("/")
    #response = test_client.get(url_for('main_bp.dashboard'))
    assert response.status_code == 200
    #response = test_client.get(response.headers['Location'])

    # Note: The user variable is not used in this test, but it's assigned to ensure the fixture runs correctly
    assert b"Please choose a category to query traffic volume on:" in response.data
   
    

def test_query(test_client, authenticated_user): 
    """
    Test query page loads with correct dropdown options
    GIVEN the user is logged in and has selected a header column to query
    WHEN the user selects a header column 
    THEN the page should load successfully and display the correct content
    """
    # Log in the user using the authenticated_user fixture
    user = authenticated_user

    response = test_client.get("/query/holiday")
    assert response.status_code == 200
    #assert b'Select a value for holiday:' in response.data
    assert b"Columbus Day" in response.data
    #assert b"New Year&#39;s Day" in response.data
    #assert b"Independence Day (Observed)" in response.data

"""
def test_query(test_client, authenticated_user):
    with test_client:
        response = test_client.get(url_for('main_bp.query', header='holiday'))
        assert response.status_code == 200
        assert b"New Year's Day" in response.data
        assert b"Independence Day (Observed)" in response.data
"""

def test_result(test_client, authenticated_user): 
    """
    Test result page loads with correct data
    GIVEN the user is logged in and has selected a header column and value to query
    WHEN the user selects a header column and value from the dropdown
    THEN the page should load successfully and display the correct content
    """
    # Log in the user using the authenticated_user fixture
    user = authenticated_user

    response = test_client.get("/result/year/2018")
    assert response.status_code == 200
    assert b"Query Results" in response.data
    assert b"You have chosen: 2018" in response.data
    assert b"Maximum Traffic Volume:</strong> 7213" in response.data
    assert b"Average Traffic Volume:</strong> 3323" in response.data
    assert b"moderate" in response.data

# note below 2 tests test different functionalities of the same route (get_all_data)
def test_get_all_data(test_client):
    """
    GIVEN no query parameters are provided
    WHEN the user requests the get_all_data route
    THEN the response should have status code 200 and contain all data in the database
    """
    # Make request without any query parameters
    response = test_client.get('/data/')

    # Check response status code and content type
    assert response.status_code == 200 #why is it a redirect?
    assert response.content_type == 'application/json'
    # Check that all data is returned when no query parameters are provided
    assert len(response.json) == Query.query.count()


def test_get_specific_data(test_client):
    """
    GIVEN multiple query parameters are provided
    WHEN the user requests the get_all_data route
    THEN the response should have status code 200 and contain the specific data in the database
    """
    # Make request with multiple query parameters, i.e. a specific date
    response = test_client.get('/data/?day=23&month=10&year=2015')
    
    # Check response status code and content type
    assert response.status_code == 200 #why is it a redirect?
    assert response.content_type == 'application/json'

    # Check that the correct data is returned when multiple query parameters are provided
    assert len(response.json) == Query.query.filter_by(day=23, month=10, year=2015).count()

