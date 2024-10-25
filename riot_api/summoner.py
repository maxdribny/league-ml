import requests
from config import Config


def get_puuid_by_riot_id(game_name, tag_line):
    """Fetches PUUID by Riot ID (game name and tag line)

    Args:
        game_name (string): The in-game name of the player.
        tag_line (string): The tag line of the player. (e.g. #EUW)
    """

    url = f"{Config.RIOT_ACCOUNT_API_URL}/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    response = requests.get(url, headers={"X-Riot-Token": Config.RIOT_API_KEY})
    response.raise_for_status()
    return response.json()["puuid"]


def get_summoner_by_puuid(puuid):
    """Fetches summoner data by PUUID

    Args:
        puuid (string): The PUUID of the player.
    """

    url = f"{Config.RIOT_ACCOUNT_API_URL}/lol/summoner/v4/summoners/by-puuid/{puuid}"
    response = requests.get(url, headers={"X-Riot-Token": Config.RIOT_API_KEY})
    response.raise_for_status()
    return response.json()
