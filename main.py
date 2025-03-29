from flask import Flask, jsonify
import lxml
import requests
from bs4 import BeautifulSoup
import re
import time
from googlesearch import search  # pip install googlesearch-python  



app = Flask(__name__)

@app.route('/')
def index():
    return "Hey there! Welcome to the Premier League API 2.0 \n\n you can use the following endpoints:\n\n /players/<player_name> \n /fixtures \n /fixtures/<team> \n /table \n\n Enjoy!"

@app.route('/players/<player_name>', methods=['GET'])
def get_player(player_name):
    try:
        # Use Google search to find the player's stats page
        query = f"{player_name} premier league.com stats"
        search_results = list(search(query, num_results=5))
        if search_results:
            res = search_results[0]
        else:
            return jsonify({"error": "No search results found for the query."}), 404

        # Adjust the URL to point to the stats page
        if "stats" in res:
            res = res.replace('stats', 'overview')
        sta = res.replace('overview', 'stats')

        # Fetch the stats page
        source = requests.get(sta).text
        page = BeautifulSoup(source, "lxml")

        # Extract player details
        name = page.find("div", class_="player-header__name t-colour").text.strip()
        position_label = page.find("div", class_="player-overview__label", string="Position")
        position = position_label.find_next_sibling("div", class_="player-overview__info").text.strip() if position_label else "Unknown"

        # Extract club information
        club = "No longer part of EPL"
        if "Club" in page.text:
            club_info = page.find_all("div", class_="info")
            if len(club_info) > 0:
                club = club_info[0].text.strip()
            if len(club_info) > 1:
                position = club_info[1].text.strip()

        # Extract detailed stats
        detailed_stats = {}
        stat_elements = page.find_all("div", class_="player-stats__stat-value")
        for stat in stat_elements:
            stat_title = stat.text.split("\n")[0].strip()
            stat_value = stat.find("span", class_="allStatContainer").text.strip()
            detailed_stats[stat_title] = stat_value

        # Extract personal details
        source2 = requests.get(res).text
        page2 = BeautifulSoup(source2, "lxml")
        personal_details = page2.find("div", class_="player-info__details-list")

        nationality = "Unknown"
        dob = "Unknown"
        height = "Unknown"

        if personal_details:
            # Extract nationality
            nationality_elem = personal_details.find("span", class_="player-info__player-country")
            nationality = nationality_elem.text.strip() if nationality_elem else "Unknown"

            # Extract Date of Birth and Height
            dob_info = personal_details.find_all("div", class_="player-info__col")
            for info in dob_info:
                label = info.find("div", class_="player-info__label").text.strip()
                if label == "Date of Birth":
                    dob = info.find("div", class_="player-info__info").text.strip()
                elif label == "Height":
                    height = info.find("div", class_="player-info__info").text.strip()

        # Return the player details as JSON
        return jsonify({
            "name": name,
            "position": position,
            "club": club,
            "key_stats": detailed_stats,
            "Nationality": nationality,
            "Date of Birth": dob,
            "Height": height
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/fixtures')
def fixtures_list():
    link = "https://onefootball.com/en/competition/premier-league-9/fixtures"
    source = requests.get(link).text
    page = BeautifulSoup(source, "lxml")
    fix = page.find_all("a", class_="MatchCard_matchCard__iOv4G")  # Updated class name

    fixtures = []
    for match in fix:
        fixture = match.get_text(separator=" ").strip()  # Use get_text with separator
        fixtures.append(fixture)

    return jsonify({"fixtures": fixtures})


@app.route('/fixtures/<team>', methods=['GET'])
def get_fixtures(team):
    link = "https://onefootball.com/en/competition/premier-league-9/fixtures"
    source = requests.get(link).text
    page = BeautifulSoup(source, "lxml")
    fix = page.find_all("a", class_="MatchCard_matchCard__iOv4G")  # Updated class name

    fixtures = []
    for match in fix:
        fixture = match.get_text(separator=" ").strip()  # Use get_text with separator
        fixtures.append(fixture)

    filtered_fixtures = [fixture for fixture in fixtures if team.lower() in fixture.lower()]

    return jsonify({"team_fixtures": filtered_fixtures})

@app.route('/table')
def table():
    link = "https://onefootball.com/en/competition/premier-league-9/table"
    source = requests.get(link).text
    page = BeautifulSoup(source, "lxml")

    # Find all rows in the standings table
    rows = page.find_all("li", class_="Standing_standings__row__5sdZG")

    # Initialize the table
    table = []
    table.append(["Position", "Team", "Played", "Wins", "Draws", "Losses", "Goal Difference", "Points"])

    # Extract data for each row
    for row in rows:
        position_elem = row.find("div", class_="Standing_standings__cell__5Kd0W")
        team_elem = row.find("p", class_="Standing_standings__teamName__psv61")
        stats = row.find_all("div", class_="Standing_standings__cell__5Kd0W")

        if position_elem and team_elem and len(stats) >= 7:
            position = position_elem.text.strip()
            team = team_elem.text.strip()
            played = stats[2].text.strip()
            wins = stats[3].text.strip()
            draws = stats[4].text.strip()
            losses = stats[5].text.strip()
            goal_difference = stats[6].text.strip()
            points = stats[7].text.strip()

            # Append the extracted data to the table
            table.append([position, team, played, wins, draws, losses, goal_difference, points])

    # Return the table as a JSON response
    return jsonify({"table": table})



if __name__ =="__main__":
    app.run(debug=True)
