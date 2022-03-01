from django.urls import path
from . import views
urlpatterns = [
        path('leagues', views.leagues, name='leagues'),
        path('teams', views.teams, name='teams'),
        path('players', views.players, name='players'),
]