import lxml
import requests
from bs4 import BeautifulSoup
import re
import time

link = f"https://onefootball.com/en/competition/premier-league-9/fixtures"
source = requests.get(link).text
page = BeautifulSoup(source, "lxml")
fix = page.find_all("a", class_="MatchCard_matchCard__iOv4G")

def fixtures_list():
    fixtures = []
    for i in range(len(fix)):
        fixtures.append(fix[i].get_text(separator=" "))  # Use get_text with separator
    
    return fixtures

def get_fixtures(team):
    fixtures = fixtures_list()
    a = []
    for i in range(len(fixtures)):
        if team in fixtures[i]:
            a.append(fixtures[i])
    return a

print(fixtures_list())