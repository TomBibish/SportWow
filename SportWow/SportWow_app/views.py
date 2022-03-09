from django.db.models import F, Q
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes , permission_classes
from rest_framework.permissions import IsAuthenticated
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
            if 'city' in request.GET and request.GET['city']:
                all_teams = all_teams.filter(city__name__icontains=request.GET['city'])
            if 'stadium' in request.GET and request.GET['stadium']:
                all_teams = all_teams.filter(stadium__name__icontains=request.GET['stadium'])
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


@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET', 'POST'])
def matches(request):
    if request.method == 'GET':
        all_matches = Match.objects.all().order_by('round', 'game_date')
        if 'round' in request.GET and request.GET['round']:
            all_matches = all_matches.filter(round=request.GET['round'])
        if 'team' in request.GET and request.GET['team']:
            all_matches = all_matches.filter((Q(away_team__name__icontains=request.GET['team']) |
                                                        Q(home_team__name__icontains=request.GET['team']) ))
        serializer = MatchSerializer(all_matches, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        round = request.data['round']
        attendance = request.data['attendance']
        game_date = request.data['game_date']
        home_team = Team.objects.get(name=request.data['home_team'])
        away_team = Team.objects.get(name=request.data['away_team'])
        home_score = request.data['home_score']
        away_score = request.data['away_score']
        new_match = Match(round=round, game_date=game_date, home_team=home_team,
                          away_team=away_team, home_score=home_score, away_score=away_score, attendance=attendance)
        home_team.goals_for = home_team.goals_for + home_score
        away_team.goals_for = away_team.goals_for + away_score
        home_team.goals_against = home_team.goals_against + away_score
        away_team.goals_against = away_team.goals_against + home_score
        if home_score == away_score:
            home_team.points = + int(1)
            away_team.points = + int(1)
        if home_score > away_score:
            home_team.points = + int(3)
        if home_score < away_score:
            away_team.points = + int(3)
        home_team.save()
        away_team.save()
        new_match.save()
        return Response(status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET', 'POST'])
def personal_watch_list(request, user_id):
    try:
        all_watch_list = PersonalWatchList.objects.filter(user=user_id)
    except PersonalWatchList.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = PersonalWatchListSerializer(all_watch_list, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = PersonalWatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET', 'PUT', 'DELETE'])
def personal_watch_list_details(request,user_id, pk):
    try:
        watch_list_details = PersonalWatchList.objects.get(pk=pk, user=user_id)
    except PersonalWatchList.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = PersonalWatchListSerializer(watch_list_details)
        return Response(serializer.data)
    if request.method == 'PUT':
        serializer = PersonalWatchListSerializer(watch_list_details, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        watch_list_details.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



