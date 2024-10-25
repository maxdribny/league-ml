import pytest
from app import app


@pytest.fixture
def client():
    """Setup the flask test client"""
    with app.test_client() as client:
        yield client


def test_home(client):
    """Test the home route ("/").

    Args:
        client (function): The test client
    """
    response = client.get("/")
    assert response.status_code == 200
    assert b"League of Legends ML App" in response.data


def test_match_stats_missing_parameters(client):
    """Test the get_match_stats route with missing parameters.

    Args:
        client (function): The test client
    """
    response = client.get("/api/match_stats")
    assert response.status_code == 400
    assert b"Game name and tagline are required query parameters" in response.data


def test_match_stats_invalid_game_count(client):
    """Test the get_match_stats route with invalid game_count parameter.

    Args:
        client (function): The test client
    """
    response = client.get("/api/match_stats?game_name=test&tagline=test&game_count=21")
    assert response.status_code == 400
    assert b"Game count to return must be between 0 and 20" in response.data
