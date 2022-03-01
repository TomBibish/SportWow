from django.shortcuts import render

# Create your views here.
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
def players(request):
    if request.method == 'GET':
        all_players = Player.objects.all()
        serializer = PlayerSerializer(all_players, many=True)
        return Response(serializer.data)