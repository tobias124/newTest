
year = '2022'

url = 'https://ticker.ligaportal.at/mannschaft/2122/spg-pitztal/tabelle'
url2 = 'https://ticker.ligaportal.at/mannschaft/2122/spg-pitztal'

import pandas as pd
import requests
from bs4 import BeautifulSoup

r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

r2 = requests.get(url2)
soup2 = BeautifulSoup(r2.text, 'html.parser')

league_table = soup.find('table', class_ = "blitz standingsTable table")
league_plan = soup2.find('table', class_ = "table table-sm teamSchedule")

# print(league_table)
teams_left = []
teams_right = []
score = []
rounds = []
dates = []

for team in league_plan.find_all('tr'):
    gl_date = team.find_all('th', class_ ="px-2")
    gl_round = team.find_all('th', class_ = "roundNr")
    gl_teams_left = team.find_all('td', class_ ="team text-left")
    gl_teams_right = team.find_all('td', class_ = "team text-right")
    gl_score = team.find_all('td', class_ = "score text-center text-nowrap px-1 px-md-3")
    for row in gl_date:
        date = row.text.strip()
        dates.append(date)
    for row in gl_round:
        round = row.find('a', class_ ="text-muted").text.strip()
        rounds.append(round)
    for row in gl_teams_left:
        team_left = row.find('a', class_= "quickInfo discreetLink text-blue-darker text-nowrap text-truncate").text.strip()  
        teams_left.append(team_left)
    for row in gl_teams_right:
        team_right = row.find('a', class_= "quickInfo discreetLink text-blue-darker text-nowrap text-truncate").text.strip()  
        teams_right.append(team_right)
    for row in gl_score:
        score.append(row.text.strip().replace("\n                        \n                    \n\n                        ", " "))

recent_games = pd.DataFrame({'Runde':rounds, 'Datum':dates, 'Heim':teams_right, '':score, 'Ausw.':teams_left})
#print(recent_games)
# print(rounds)
# print(dates)
# print(teams_left)
# print(teams_right)
# print(score)

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

#print(glw_table) 
 