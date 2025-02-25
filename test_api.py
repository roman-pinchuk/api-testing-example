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


def test_create_post():
    """"Test to create a post"""

    payload = {
        "title": "API Testing with Dev Containers",
        "body": "This is a test post created using API testing.",
        "userId": 1
    }

    response = requests.post(f"{BASE_URL}/posts", json=payload)
    # Validate status code
    assert response.status_code == 201

    # Validarte response contains the same data
    response_data = response.json()

    assert response_data["title"] == payload["title"]
    assert response_data["body"] == payload["body"]
    assert response_data["userId"] == payload["userId"]
    assert "id" in response_data  # The new post should have an ID
