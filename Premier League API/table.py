import lxml
import requests
from bs4 import BeautifulSoup
import re
import time
from pprint import pprint



link = f"https://onefootball.com/en/competition/premier-league-9/table"
source = requests.get(link).text
page = BeautifulSoup(source, "lxml")
tab = page.find_all("a", class_="standings__row-grid")

table = []
table.append("  ________________ PL W D L GD PTS")



for i in range(len(tab)):
    table.append(tab[i].text.strip())

pprint(table)
