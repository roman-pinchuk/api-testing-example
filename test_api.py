import requests
import requests_mock
import pytest
import tenacity
from tenacity import retry, stop_after_attempt, wait_fixed, wait_exponential


def test_get_posts(base_url):
    """Test to fetch all posts"""
    response = requests.get(f"{base_url}/posts", timeout=10)
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

    response = requests.post(f"{base_url}/posts", json=payload, timeout=10)
    # Validate status code
    assert response.status_code == 201

    # Validate response contains the same data
    response_data = response.json()

    assert response_data["title"] == payload["title"]
    assert response_data["body"] == payload["body"]
    assert response_data["userId"] == payload["userId"]
    assert "id" in response_data  # The new post should have an ID


@pytest.mark.parametrize("endpoint", ["posts", "comments", "albums"])
def test_get_resources(base_url, endpoint):
    """Test to fetch resources"""
    response = requests.get(f"{base_url}/{endpoint}", timeout=10)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_authenticated_request(base_url, auth_token):
    """Test an authenticated request"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.get(f"{base_url}/posts/1", headers=headers, timeout=10)

    assert response.status_code in [200, 403]
    assert isinstance(response.json(), dict)


def test_mocked_get_request(base_url):
    """Test API call with a mocked response"""

    with requests_mock.Mocker() as mock:
        payload = {"id": 1, "title": "Mocked Title"}

        mock.get(f"{base_url}/posts/1", json=payload)

        response = requests.get(f"{base_url}/posts/1", timeout=10)

        assert response.status_code == 200
        assert response.json() == payload


def test_mocked_post_request(base_url):
    """Test API POST request with a mocked response"""
    with requests_mock.Mocker() as mock:
        mock.post(f"{base_url}/posts", status_code=201, json={"id": 101})

        payload = {"title": "New Post",
                   "body": "Testing post request", "userId": 1}
        response = requests.post(f"{base_url}/posts", json=payload, timeout=10)

        assert response.status_code == 201
        assert response.json() == {"id": 101}


def test_api_timeout(base_url):
    """Test handling API timeouts"""
    with requests_mock.Mocker() as mock:
        mock.get(f"{base_url}/posts/1", exc=requests.exceptions.Timeout)

        with pytest.raises(requests.exceptions.Timeout):
            requests.get(f"{base_url}/posts/1", timeout=0.01)


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def fetch_post(base_url):
    """Retries API request up to 3 times with a 2-second wait"""
    response = requests.get(f"{base_url}/posts/1", timeout=2)

    if response.status_code != 200:
        raise requests.exceptions.RequestException(
            f"API failed with status {response.status_code}")
    return response.json()


def test_api_retry(base_url):
    """Test API retries in case of failure"""
    with requests_mock.Mocker() as mock:
        mock.get(f"{base_url}/posts/1", status_code=500)

        with pytest.raises(tenacity.RetryError):
            fetch_post(base_url)


@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=1, max=10))
def fetch_with_backoff(base_url):
    """Retries API request with exponential backoff"""
    response = requests.get(f"{base_url}/posts/1", timeout=10)

    if response.status_code == 429:
        raise requests.exceptions.RequestException("Rate limit exceeded")
    return response.json()


def test_fetch_with_backoff(base_url):
    """Test API retries with exponential backoff in case of failure"""
    with requests_mock.Mocker() as mock:
        mock.get(f"{base_url}/posts/1", status_code=429)

        with pytest.raises(tenacity.RetryError):
            fetch_with_backoff(base_url)
