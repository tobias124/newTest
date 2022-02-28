
year = '2022'

url = 'https://ticker.ligaportal.at/mannschaft/2122/spg-pitztal/tabelle'

import pandas as pd
import requests
from bs4 import BeautifulSoup

r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

league_table = soup.find('table', class_ = "blitz standingsTable table")

# print(league_table)


teams = []
ranks = []
games_played = []
points = []

for team in league_table.find_all('tr'):
    if team != None:
        gl_team_rows = team.find_all('td', class_= "team")
        gl_tableRank = team.find('td', class_ = "center tableRank")
        gl_gamesPlayed = team.find('td', class_ = "center gamesPlayed")
        gl_points = team.find('td', class_ = "center points")
    for t in gl_team_rows:
        gl_team = t.find('a', class_= "quickInfo discreetLink").text.strip()
        teams.append(gl_team)
        if gl_tableRank != None:
            ranks.append(gl_tableRank.text.strip() + ".")
        if gl_gamesPlayed != None:
            games_played.append(gl_gamesPlayed.text.strip())
        if gl_points != None:
            points.append(gl_points.text.strip())

# print(ranks)        
# print(teams)
# print(games_played)
# print(points)

glw_table = pd.DataFrame({'R':ranks, 'Mannschaft':teams, 'Sp.':games_played, 'P':points})

print(glw_table) 
 