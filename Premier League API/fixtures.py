import lxml
import requests
from bs4 import BeautifulSoup
import re
import time



link = f"https://onefootball.com/en/competition/premier-league-9/fixtures"
source = requests.get(link).text
page = BeautifulSoup(source, "lxml")
fix = page.find_all("li", class_="simple-match-cards-list__match-card")


def fixtures_list():
    fixtures = []
    for i in range(len(fix)):
        fixtures.append(fix[i].text.strip())
    
    return fixtures


def get_fixtures(team):
    fixtures = fixtures_list()
    a = []
    for i in range(len(fixtures)):
        if team in fixtures[i]:
            a.append(fixtures[i])
    return a
    


print(get_fixtures("Arsenal"))