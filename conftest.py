import pytest


@pytest.fixture
def base_url():
    return "https://jsonplaceholder.typicode.com"


@pytest.fixture
def auth_token():
    """Fixture for auth token"""
    return "someCoolTokenHere"
