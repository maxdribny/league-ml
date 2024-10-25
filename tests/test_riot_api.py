import pytest
import requests_mock
from riot_api.summoner import get_puuid_by_riot_id, get_summoner_by_puuid
from riot_api.match import get_recent_match_ids_by_puuid, get_match_details_by_id


@pytest.fixture
def mock_requests():
    """Setup requests to mock Riot API Responses."""
    with requests_mock.Mocker() as mock:
        yield mock


def test_get_puuid_by_riot_id(mock_requests):
    """Test get_puuid_by_riot_id function with mocked response."""
    game_name = "SomeName"
    tag_line = "EUW"
    mock_url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    mock_puuid = "mock-puuid"

    # Mock the Riot API Response
    mock_requests.get(mock_url, json={"puuid": mock_puuid})

    puuid = get_puuid_by_riot_id(game_name, tag_line)
    assert puuid == mock_puuid


def test_get_recent_match_ids_by_puuid(mock_requests):
    """Test get_recent_match_ids_by_puuid function with mocked response."""
    puuid = "mock-puuid"
    game_count = 2
    mock_url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?count={game_count}"
    mock_match_ids = ["mock-match-id-1", "mock-match-id-2"]

    # Mock the Riot API Response
    mock_requests.get(mock_url, json=mock_match_ids)

    match_ids = get_recent_match_ids_by_puuid(puuid, game_count)
    assert match_ids == mock_match_ids


def test_get_match_details_by_id(mock_requests):
    """Test get_match_details_by_id function with mocked response."""
    match_id = "mock-match-id"
    mock_url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}"
    mock_match_details = {
        "gameId": 1234567890,
        "participants": [{"summonerName": "Player1", "championName": "Ahri"}],
    }

    # Mock the Riot API Response
    mock_requests.get(mock_url, json=mock_match_details)

    match_details = get_match_details_by_id(match_id)
    assert match_details == mock_match_details
    assert match_details["gameId"] == 1234567890
    assert match_details["participants"][0]["summonerName"] == "Player1"
