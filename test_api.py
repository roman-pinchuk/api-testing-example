import requests
import pytest

BASE_URL = "https://jsonplaceholder.typicode.com"

def test_get_posts():
    """Test to fetch all posts"""
    response = requests.get(f"{BASE_URL}/posts")
    
    # Validate HTTP status code
    assert response.status_code == 200

    # Validate response type is a list
    assert isinstance(response.json(), list)
