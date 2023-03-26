
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
    response = test_client.get("/")
    #response = test_client.get(url_for('main_bp.dashboard'))
    assert response.status_code == 200
    #response = test_client.get(response.headers['Location'])
    assert b"Please choose a category to query traffic volume on:" in response.data
   
    

def test_query(test_client, authenticated_user): 
    """
    Test query page loads with correct dropdown options
    GIVEN the user is logged in and has selected a header column to query
    WHEN the user selects a header column 
    THEN the page should load successfully and display the correct content
    """
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
    response = test_client.get("/result/year/2018")
    assert response.status_code == 200
    assert b"Query Results" in response.data
    assert b"Chosen Option:</strong> 2018" in response.data
    assert b"Average Traffic Volume:</strong> 3323" in response.data
    assert b"Maximum Traffic Volume:</strong> 7213" in response.data

def test_get_all_data(test_client, authenticated_user):
    """Test the get_all_data route"""
    response = test_client.get('/data/')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert len(response.json) == Query.query.count()




"""
def test_result(test_client, authenticated_user):
    with test_client:
        response = test_client.get(url_for('main_bp.result', header='year', option='2018'))
        assert response.status_code == 200
        assert b"Chosen Option: 2018" in response.data
        assert b"Average traffic volume:" in response.data
        assert b"Minimum traffic volume:" in response.data
        assert b"Maximum traffic volume:" in response.data
"""


"""
from flask_login import current_user
from flask.testing import FlaskClient
    assert b'Average Traffic Volume: 500' in response.data
    assert b'Minimum Traffic Volume: 200' in response.data
    assert b'Maximum Traffic Volume: 1000' in response.data

# Test the logout route
def test_logout(client: FlaskClient):
    # GIVEN the user is logged in
    with client:
        client.post('/login', data={'email': 'user@example.com', 'password': 'password'})
    
    # WHEN the user logs out
    response = client.get('/logout', follow_redirects=True)
    
    # THEN the page should load successfully and display the correct content
    assert response.status_code == 200
    assert b'Log In' in response.data
    assert b'You have been logged out.' in response.data

"""