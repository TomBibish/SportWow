from django.urls import path
from . import views
urlpatterns = [
        path('leagues', views.leagues, name='leagues'),
        path('teams', views.teams, name='teams'),
        path('players', views.players, name='players'),
        path('leagues/<int:league_id>', views.league_teams),
        path('stadiums', views.stadiums, name='stadiums'),
        path('matches', views.matches, name='matches'),
        path('personal_watch_list/<int:user_id>', views.personal_watch_list),
        path('personal_watch_list/<int:user_id>/<int:pk>', views.personal_watch_list_details)
]