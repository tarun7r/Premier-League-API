import lxml
import requests
from bs4 import BeautifulSoup
from googlesearch import search  # pip install googlesearch-python
import re

# Input player name
player_name = "ronaldo"

# Using googlesearch to find Premier League stats for the player
query = f"{player_name} premier league.com stats"
search_results = list(search(query, num_results=5))
if search_results:
    res = search_results[0]
else:
    raise ValueError("No search results found for the query.")

# Adjust the URL to point to the stats page
if "stats" in res:
    res = res.replace('stats', 'overview')

sta = res.replace('overview', 'stats')

# Fetch the stats page
source = requests.get(sta).text
page = BeautifulSoup(source, "lxml")

# Extract player details
name = page.find("div", class_="player-header__name t-colour").text
name = re.sub(r'\s+', ' ', name).strip()  # Replace multiple spaces/newlines with a single space
print(f"Player Name: {name}")

position_label = page.find("div", class_="player-overview__label", string="Position")
if position_label:
    position = position_label.find_next_sibling("div", class_="player-overview__info").text.strip()
    print(f"Position: {position}")
else:
    position = "Unknown"

# Extract club information
club = "No longer part of EPL"
if "Club" in page.text:
    club_info = page.find_all("div", class_="info")
    if len(club_info) > 0:
        club = club_info[0].text.strip()
    if len(club_info) > 1:
        position = club_info[1].text.strip()
print(f"Club: {club}")

# Extract detailed stats
detailed_stats = {}
stat_elements = page.find_all("div", class_="player-stats__stat-value")
for stat in stat_elements:
    stat_title = stat.text.split("\n")[0].strip()
    stat_value = stat.find("span", class_="allStatContainer").text.strip()
    detailed_stats[stat_title] = stat_value

print("\nDetailed Stats:")
for key, value in detailed_stats.items():
    print(f"{key}: {value}")

# Extract personal details
source2 = requests.get(res).text
page2 = BeautifulSoup(source2, "lxml")
personal_details = page2.find("div", class_="player-info__details-list")

if personal_details:
    # Extract nationality
    nationality = personal_details.find("span", class_="player-info__player-country")
    nationality = nationality.text.strip() if nationality else "Unknown"
    
    # Extract Date of Birth
    dob = "Unknown"
    dob_info = personal_details.find_all("div", class_="player-info__col")
    for info in dob_info:
        label = info.find("div", class_="player-info__label").text.strip()
        if label == "Date of Birth":
            dob = info.find("div", class_="player-info__info").text.strip()
            break
    
    # Extract Height
    height = "Unknown"
    for info in dob_info:
        label = info.find("div", class_="player-info__label").text.strip()
        if label == "Height":
            height = info.find("div", class_="player-info__info").text.strip()
            break

    print("\nPersonal Details:")
    print(f"Nationality: {nationality}")
    print(f"Date of Birth: {dob}")
    print(f"Height: {height}")
else:
    print("Personal details not found.")