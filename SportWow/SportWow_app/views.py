from django.db.models import F, Q
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import *
from .serializers import *
from.custom_queries import *


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
def team_details(request, team_name):
    if request.method == 'GET':
        try:
            team = Team.objects.get(name=team_name)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TeamSerializer(team)
        return Response(serializer.data)


@api_view(['GET'])
def team_coach(request, team_name):
    if request.method == 'GET':
        try:
            coach = TeamCoach.objects.get(team__name=team_name, is_active=True)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TeamCoachSerializer(coach)
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


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def matches(request):
    if request.method == 'GET':
        all_matches = Match.objects.all().order_by('-round', 'game_date')
        if 'round' in request.GET and request.GET['round']:
            all_matches = all_matches.filter(round=request.GET['round'])
        if 'team' in request.GET and request.GET['team']:
            all_matches = all_matches.filter((Q(away_team__name__icontains=request.GET['team']) |
                                                Q(home_team__name__icontains=request.GET['team'])))
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
            home_team.points = home_team.points + int(1)
            away_team.points = away_team.points + int(1)
        if home_score > away_score:
            home_team.points = home_team.points + int(3)
        if home_score < away_score:
            away_team.points = away_team.points + int(3)
        home_team.save()
        away_team.save()
        new_match.save()
        return Response(status=status.HTTP_201_CREATED)



        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def compare_players(request):
    player1_first_name = request.GET.get('player1_first_name')
    player1_last_name = request.GET.get('player1_last_name')
    player2_first_name = request.GET.get('player2_first_name')
    player2_last_name = request.GET.get('player2_last_name')
    print('player1_first_name' + player1_first_name)
    result = compare_two_players(player1_first_name, player1_last_name, player2_first_name, player2_last_name)
    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
def compare_teams(request):
    team1 = request.GET.get('team1')
    team2 = request.GET.get('team2')
    league = request.GET.get('league')
    result = compare_two_teams(team1, team2, league)
    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
def league_table(request):
    league = request.GET.get('league')
    result = show_league_table(league)
    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
def league_assists(request):
    league = request.GET.get('league')
    result = show_league_assists(league)
    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
def league_goals(request):
    league = request.GET.get('league')
    result = show_league_goals(league)
    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
def crowd_avg(request):
    team = request.GET.get('team')
    result = show_crowd_avg(team)
    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
def team_players(request, team_name):
    result = show_players_for_team(team_name)
    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
def league_players(request, league_id):
    result = show_players_for_league(league_id)
    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
def matches_rounds(request):
    result = get_rounds()
    return Response(result, status=status.HTTP_200_OK)



obtain_auth_token = ObtainAuthToken.as_view()


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def sign_out(request):
    token1 = Token.objects.get(key=request.auth)
    token1.delete()
    return 'Deleted successfully'


@api_view(['POST'])
def register(request):
    # if request.method == 'GET':
    #     users = User.objects.all()
    #     users_list = [user for user in users]
    #     serializer = UserSerializer(users_list, many=True)
    #     print(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "successfully added"
            data['email'] = user.email
            data['username'] = user.username
        else:
            data = serializer.errors
        return Response(data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def current_user(request):
    curr_user = request.user
    data = {
        "first_name": curr_user.first_name,
        "last_name": curr_user.last_name,
        "id": curr_user.id,
        "username":curr_user.username
    }
    return Response(data)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET', 'POST'])
def tickets(request):
    if request.method == 'GET':
        all_tickets = Ticket.objects.all()
        serializer = TicketSerializer(all_tickets,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'POST':
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
@api_view(['GET', 'PUT', 'DELETE'])
def ticket_details(request, pk):
    try:
        ticket = Ticket.objects.get(pk=pk)
    except ticket.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TicketSerializer(ticket)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'PUT':
        serializer = TicketSerializer(ticket, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        ticket.delete()
        return Response("Deleted Successfully")


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET', 'POST'])
def ordered_tickets(request):
    if request.method == 'GET':
        all_ordered_tickets = OrderedTicket.objects.all()
        serializer = OrderedTicketSerializer(all_ordered_tickets,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'POST':
        serializer = OrderedTicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
