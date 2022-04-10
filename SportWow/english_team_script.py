import json
import requests as requests
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SportWow.settings")
import django
django.setup()
from SportWow_app.models import *

url = "https://api.football-data-api.com/league-teams?key=$$$$$$$$&season_id=2012&include=stats"
res = requests.get(url)
response = json.loads(res.text)
teams = []
# for team in response['data']:
#     # print(team['name'],None, team['country'], team['image'],None, 'Premier League'
#     #       ,0, ":", team['stats']['seasonConcededNum_overall'],(round(team['stats']['seasonPPG_overall']*38)))
#     new_team = Team(name=team['name'],country_id=2,league_id=2, picture_url=team['image']
#                     ,points=(round(team['stats']['seasonPPG_overall']*38)),
#                     goals_for=team['stats']['seasonGoals_overall'],
#                     goals_against=team['stats']['seasonConcededNum_overall'])
#     new_team.save()
#     print(new_team)
