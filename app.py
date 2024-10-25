from flask import Flask, jsonify, request
import requests
import json

app = Flask(__name__)

# Set up Riot API key
RIOT_API_KEY = "RGAPI-d830ba01-0db4-4b83-80d3-8c40d9a9bc6a"

# Base URL for the RIOT API
RIOT_API_URL = "https://europe.api.riotgames.com"


@app.route("/")
def home():
    return "League of Legends ML App"


# Endpoint to get recent match stats
@app.route("/api/match_stats", methods=["GET"])
def get_match_stats():
    game_name = request.args.get("game_name")
    tagline = request.args.get("tagline")
    game_count = request.args.get("game_count", default=1, type=int)

    # Validate that game_count is between 0 and 20
    if not (0 <= game_count <= 20):
        return jsonify({"error": "game_count must be between 0 and 20"}), 400

    if not game_name or not tagline:
        return jsonify({"error": "Game name and tagline are required"}), 400

    try:
        # Step 1: Get PUUID using the Riot ID
        summoner_url = (
            f"{RIOT_API_URL}/riot/account/v1/accounts/by-riot-id/{game_name}/{tagline}"
        )
        response = requests.get(summoner_url, headers={"X-Riot-Token": RIOT_API_KEY})
        response.raise_for_status()
        account_data = response.json()

        puuid = account_data["puuid"]

        # 2. Get Recent match history using the PUUID
        # We can specify count = 1 to get only the most recent match
        match_ids_url = f"{RIOT_API_URL}/lol/match/v5/matches/by-puuid/{puuid}/ids?count={game_count}"
        match_ids_response = requests.get(
            match_ids_url, headers={"X-Riot-Token": RIOT_API_KEY}
        )
        match_ids_response.raise_for_status()
        match_ids = match_ids_response.json()

        if not match_ids:
            return jsonify({"error": "No recent matches found for this player"}), 404

        # Get the most recent match ID
        match_id = match_ids[0]

        # 3. Get match details for each match ID
        matches = []
        for match_id in match_ids:
            match_detail_url = f"{RIOT_API_URL}/lol/match/v5/matches/{match_id}"
            match_detail_response = requests.get(
                match_detail_url, headers={"X-Riot-Token": RIOT_API_KEY}
            )
            match_detail_response.raise_for_status()
            match_detail = match_detail_response.json()
            matches.append(match_detail)

        # 4. Dump match detail JSON data to a file
        with open("match_data.json", "w") as json_file:
            json.dump(
                matches, json_file, indent=4
            )  # Dumping json data into a file with indentation

        return jsonify(match_detail), 200

    except requests.exceptions.RequestException as e:
        # Print the error to console to inspect it
        print(f"Error: {e.response.text}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
