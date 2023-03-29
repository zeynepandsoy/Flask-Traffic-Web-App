
from traffic_app.models import Query
from flask import url_for

# -----------------
# Test Main Routes
# -----------------


def test_dashboard(test_client, authenticated_user): 
    """
    Test dashboard/main page is accessible when logged in
    GIVEN the user is logged in
    WHEN the user requests the main page
    THEN the main page should load successfully and display the correct content (column headers)
    """
    # Log in the user using the authenticated_user fixture
    # Note: The user variable is not used in this test, but it's assigned to ensure the fixture runs correctly
    user = authenticated_user

    # Make a request to the main page
    #response = test_client.get(url_for('main_bp.dashboard'))
    response = test_client.get("/") 
    
    # Check that the response is valid
    assert response.status_code == 200

    # Check that the response data contains the expected HTML
    assert b"Please choose a category to query traffic volume on:" in response.data
   
    

def test_query(test_client, authenticated_user): 
    """
    Test query page loads with correct dropdown options
    GIVEN an authenticated user that has logged in 
    WHEN the user selects a header column to query (dashboard page)
    THEN the query page should load successfully and display the correct content (dropdown options)
    """
    # Log in the user using the authenticated_user fixture
    user = authenticated_user

    # Make a request to the query page
    #response = test_client.get("/query/holiday") 
    response = test_client.get(url_for('main_bp.query', header='holiday')) 

    # Check that the response is valid
    assert response.status_code == 200

    # Check that the response data contains the expected HTML
    assert b"Columbus Day" in response.data
    



def test_result(test_client, authenticated_user): 
    """
    Test result page loads with correct data
    GIVEN an authenticated user that is logged in 
    WHEN the user selects a header column and option from the dropdown (query page)
    THEN the result page should load successfully and display the correct results
    """
    # Log in the user using the authenticated_user fixture
    user = authenticated_user

    # Make a request to the result page
    #response = test_client.get("/result/year/2018")
    response = test_client.get(url_for('main_bp.result', header='year', option='2018'))

    # Check that the response is valid
    assert response.status_code == 200

    # Check that the response data contains the expected HTML
    assert b"Query Results" in response.data
    assert b"You have chosen the year: 2018" in response.data
    assert b"Maximum Traffic Volume:</strong> 7213" in response.data
    assert b"Average Traffic Volume:</strong> 3323" in response.data
    assert b"moderate" in response.data


# ---------------
# Test API Route
# ---------------
# Below 2 tests test different functionalities of the same route (get_all_data) which does not require authentication

def test_get_all_data(test_client):
    """
    GIVEN no query parameters are provided
    WHEN the user requests the get_all_data route
    THEN the response should succesfully return all data in the database in JSON format
    """
    # Make request without any query parameters
    response = test_client.get('/data/')

    # Check that the response status code was successful
    assert response.status_code == 200 

    # Check that response content is in JSON format
    assert response.content_type == 'application/json'

    # Check that all data is returned when no query parameters are provided
    assert len(response.json) == Query.query.count()


def test_get_specific_data(test_client):
    """
    GIVEN multiple query parameters are provided
    WHEN the user requests the get_all_data route
    THEN the response should succesfully return the specific data in the database in JSON format
    """
    # Make request with multiple query parameters, i.e. a specific date
    response = test_client.get('/data/?day=23&month=10&year=2015')
    
    # Check that the response status code was successful
    assert response.status_code == 200 

    # Check that response content is in JSON format
    assert response.content_type == 'application/json'

    # Check that the correct data is returned when multiple query parameters are provided
    assert len(response.json) == Query.query.filter_by(day=23, month=10, year=2015).count()

