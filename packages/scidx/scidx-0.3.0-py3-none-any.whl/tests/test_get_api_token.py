import pytest
from requests.exceptions import HTTPError
from scidx.client import sciDXClient

# Test for successfully retrieving an API token
def test_get_api_token_success():
    """
    Test that the get_api_token function correctly retrieves an 
    access token when the authentication is successful.
    """
    # Create a client instance with the actual API URL
    client = sciDXClient(api_url="http://localhost:8765")
    
    # Call the get_api_token method with the real credentials
    token = client.get_api_token(username="test", password="test")
    
    # Check that the token is not None or empty
    assert token is not None
    assert len(token) > 0

# Test for failed API token retrieval due to incorrect credentials
def test_get_api_token_failure():
    """
    Test that the get_api_token function raises an HTTPError when 
    the authentication fails due to incorrect credentials.
    """
    # Create a client instance with the actual API URL
    client = sciDXClient(api_url="http://localhost:8765")
    
    # Attempt to retrieve the token with incorrect credentials
    with pytest.raises(HTTPError) as exc_info:
        client.get_api_token(username="wrong_user", password="wrong_password")
    
    # Check that the exception is indeed an HTTPError
    assert isinstance(exc_info.value, HTTPError)
    
    # Check that the status code in the error is 401 (Unauthorized)
    assert exc_info.value.response.status_code == 401
    
    # Check that the exception message contains 'Unauthorized'
    assert "Unauthorized" in str(exc_info.value)