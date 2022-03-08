from django.db.models import F
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
from .serializers import *


@api_view(['GET'])
def leagues(request):
    if request.method == 'GET':
        all_leagues = League.objects.all()
        serializer = LeagueSerializer(all_leagues, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def teams(request):
    if request.method == 'GET':
        all_teams = Team.objects.all()
        serializer = TeamSerializer(all_teams, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def league_teams(request, league_id):
    if request.method == 'GET':
        try:
            all_teams = Team.objects.filter(league=league_id).order_by('-points',
                                                                       -(F('goals_for') - F('goals_against')),
                                                                       '-goals_for')
        except all_teams.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TeamSerializer(all_teams, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def players(request):
    if request.method == 'GET':
        all_players = Player.objects.all()
        serializer = PlayerSerializer(all_players, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def stadiums(request):
    if request.method == 'GET':
        all_stadiums = Stadium.objects.all().order_by('-capacity')
        serializer = StadiumSerializer(all_stadiums, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def matches(request):
    if request.method == 'GET':
        all_matches = Match.objects.all().order_by('round')
        if 'round' in request.GET and request.GET['round']:
            all_matches = all_matches.filter(round=request.GET['round'])
        serializer = MatchSerializer(all_matches, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        round = request.data['round']
        game_date = request.data['game_date']
        home_team = Team.objects.get(name=request.data['home_team'])
        away_team = Team.objects.get(name=request.data['away_team'])
        home_score = request.data['home_score']
        away_score = request.data['away_score']
        new_match = Match(round=round, game_date=game_date, home_team=home_team,
                          away_team=away_team, home_score=home_score, away_score=away_score)
        home_team.goals_for = home_team.goals_for + home_score
        away_team.goals_for = away_team.goals_for + away_score
        home_team.goals_against = home_team.goals_against + away_score
        away_team.goals_against = away_team.goals_against + home_score
        if home_score == away_score:
            print("Draw")
            print(f"home_team.points before {home_team.points}")
            home_team.points = + int(1)
            away_team.points = + int(1)
            print(f"home_team.points after {home_team.points}")
        if home_score > away_score:
            print("Draw")
            print("Home Team Won")
            home_team.points = + int(3)
        if home_score < away_score:
            print("Away Team Won")
            away_team.points = + int(3)
        home_team.save()
        away_team.save()
        new_match.save()
        return Response(status=status.HTTP_400_BAD_REQUEST)


