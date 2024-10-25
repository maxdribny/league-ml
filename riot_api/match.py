import requests
from config import Config


def get_recent_match_ids_by_puuid(puuid, game_count=1):
    """Fetches recent match IDs by PUUID. Allows parameterization of game_count to return multiple matches.

    Args:
        puuid (string): The PUUID of the player.
        game_count (int, optional): Number of recent matches to return. Defaults to 1.
    """
    if game_count < 0 or game_count > 20:
        raise ValueError("game_count must be between 0 and 20")

    url = f"{Config.RIOT_MATCH_API_URL}/lol/match/v5/matches/by-puuid/{puuid}/ids?count={game_count}"
    response = requests.get(url, headers={"X-Riot-Token": Config.RIOT_API_KEY})
    response.raise_for_status()
    return response.json()


def get_match_details_by_id(match_id):
    """Fetches match details by match ID.

    Args:
        match_id (string): The match ID.
    """
    url = f"{Config.RIOT_MATCH_API_URL}/lol/match/v5/matches/{match_id}"
    response = requests.get(url, headers={"X-Riot-Token": Config.RIOT_API_KEY})
    response.raise_for_status()
    return response.json()
