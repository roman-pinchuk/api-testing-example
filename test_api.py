import requests
import pytest


def test_get_posts(base_url):
    """Test to fetch all posts"""
    response = requests.get(f"{base_url}/posts")
    # Validate HTTP status code
    assert response.status_code == 200
    # Validate response type is a list
    assert isinstance(response.json(), list)


def test_create_post(base_url):
    """"Test to create a post"""

    payload = {
        "title": "API Testing with Dev Containers",
        "body": "This is a test post created using API testing.",
        "userId": 1
    }

    response = requests.post(f"{base_url}/posts", json=payload)
    # Validate status code
    assert response.status_code == 201

    # Validarte response contains the same data
    response_data = response.json()

    assert response_data["title"] == payload["title"]
    assert response_data["body"] == payload["body"]
    assert response_data["userId"] == payload["userId"]
    assert "id" in response_data  # The new post should have an ID


@pytest.mark.parametrize("endpoint", ["posts", "comments", "albums"])
def test_get_resources(base_url, endpoint):
    """Test to fetch resources"""
    response = requests.get(f"{base_url}/{endpoint}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_authenticated_request(base_url, auth_token):
    """Test an authenticated request"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.get(f"{base_url}/posts/1", headers=headers)

    assert response.status_code in [200, 403]
    assert isinstance(response.json(), dict)
