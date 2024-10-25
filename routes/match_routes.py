from flask import Blueprint, jsonify, request
from riot_api.summoner import get_puuid_by_riot_id, get_summoner_by_puuid
from riot_api.match import get_recent_match_ids_by_puuid, get_match_details_by_id
import requests
import json

# Creata a Blueprint for the match routes
match_routes = Blueprint("match_routes", __name__)


@match_routes.route("/api/match_stats", methods=["GET"])
def get_match_stats():
    game_name = request.args.get("game_name")
    tagline = request.args.get("tagline")
    game_count = request.args.get("game_count", default=1, type=int)

    # Validate that game_count is between 0 and 20
    if not (0 <= game_count <= 20):
        return jsonify({"error": "Game count to return must be between 0 and 20"}), 400

    if not game_name or not tagline:
        return (
            jsonify({"error": "Game name and tagline are required query parameters"}),
            400,
        )

    try:
        # 1. Get PUUID using the Riot ID (game name and tagline)
        puuid = get_puuid_by_riot_id(game_name, tagline)

        # 2. Get recent match IDs by PUUID
        match_ids = get_recent_match_ids_by_puuid(puuid, game_count)

        if not match_ids:
            return jsonify({"error": "No recent matches found for the player"}), 404

        # 3. Get match details for each match ID
        matches = []
        for match_id in match_ids:
            match_detail = get_match_details_by_id(match_id)
            matches.append(match_detail)

        # 4. Return match data in JSON format
        with open("match_details.json", "w") as f:
            json.dump(matches, f, indent=4)
        return jsonify(matches), 200

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
