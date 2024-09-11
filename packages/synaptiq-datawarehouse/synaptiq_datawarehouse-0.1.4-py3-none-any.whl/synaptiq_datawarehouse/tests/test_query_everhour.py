import pytest
import requests
from unittest.mock import patch
from synaptiq_datawarehouse.integrations import query_everhour  # Adjust the import path as necessary

def test_query_everhour_success():
    # Mock the requests.get to return a successful response
    with patch('requests.get') as mocked_get:
        mocked_get.return_value.status_code = 200
        mocked_get.return_value.text = 'Success'
        
        response = query_everhour('/projects', 'dummy_api_key')
        
        assert response == 'Success'
        mocked_get.assert_called_once_with(
            'https://api.everhour.com/projects', 
            headers={
                'Content-Type': 'application/json',
                'X-Api-Key': 'dummy_api_key'
            }
        )

def test_query_everhour_http_error():
    # Mock the requests.get to simulate an HTTP error
    with patch('requests.get') as mocked_get:
        mocked_get.return_value.status_code = 404
        mocked_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError
        
        with pytest.raises(requests.exceptions.HTTPError):
            query_everhour('/nonexistent', 'dummy_api_key')

def test_query_everhour_request_exception():
    # Mock requests.get to simulate a RequestException
    with patch('requests.get') as mocked_get:
        mocked_get.side_effect = requests.exceptions.RequestException
        
        response = query_everhour('/failure', 'dummy_api_key')
        
        # Check that the exception is logged and the function doesn't raise an exception
        # This assumes that your function logs errors and suppresses exceptions, as indicated
        assert response is None

