import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

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

# Print the table in a pretty format
print(tabulate(table, headers="firstrow", tablefmt="grid"))