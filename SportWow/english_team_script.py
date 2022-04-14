import json
from datetime import datetime

import requests as requests
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SportWow.settings")
import django
django.setup()
from SportWow_app.models import *

# url = "https://api.football-data-api.com/league-teams?key=$$$$$$$$&season_id=2012&include=stats"
# res = requests.get(url)
# response = json.loads(res.text)
# teams = []
# for team in response['data']:
#     # print(team['name'],None, team['country'], team['image'],None, 'Premier League'
#     #       ,0, ":", team['stats']['seasonConcededNum_overall'],(round(team['stats']['seasonPPG_overall']*38)))
#     new_team = Team(name=team['name'],country_id=2,league_id=2, picture_url=team['image']
#                     ,points=(round(team['stats']['seasonPPG_overall']*38)),
#                     goals_for=team['stats']['seasonGoals_overall'],
#                     goals_against=team['stats']['seasonConcededNum_overall'])
#     new_team.save()
#     print(new_team)
players_url = 'https://api.football-data-api.com/league-players?key=example&season_id=2012&page=4'
res = requests.get(players_url)
response = json.loads(res.text)
players = []
teams_dict = {151: 30,
              159: 36,
              153: 32,
              93: 22,
              148: 28,
              251: 39,
              145: 26,
              146: 27,
              143: 24,
              144: 25,
              155: 33,
              209: 37,
              92: 21,
              158: 35,
              108: 23,
              223: 38,
              157: 34,
              59: 20,
              149: 29,
              152: 31
              }
for player in response['data']:
    pic = f'https://cdn.footystats.org/img/players/{player["nationality"].lower()}' \
          f'-{player["first_name"].lower()}-{player["last_name"].lower()}.png'
    # print(f"{player['first_name']} {player['last_name']} ")
    # print(pic)
    # print(datetime.fromtimestamp(player['birthday']))
    # print(f"Apps: {player['appearances_overall']},"
    #       f" Goals: {player['goals_overall']},"
    #       f" Assists: {player['assists_overall']},"
    #       f"Yellow Cards: {player['yellow_cards_overall']},"
    #       f"Red Cards: {player['red_cards_overall']} ")
    # print(teams_dict[player['club_team_id']])
    player1 = Player(first_name=player['first_name'], last_name=player['last_name'],
                    country_id=2, picture_url=pic, birth_date=(datetime.fromtimestamp(player['birthday'])))
    player1.save()
    team_id_number = teams_dict[(player['club_team_id'])]
    team_player = TeamPlayer(player_id=player1.id, is_active=True,
                             team_id=team_id_number,
                             goals=player['goals_overall'],
                             appearances=player['appearances_overall'],
                             assists=player['assists_overall'],
                             red_cards=player['red_cards_overall'],
                             yellow_cards=player['yellow_cards_overall'])
    team_player.save()