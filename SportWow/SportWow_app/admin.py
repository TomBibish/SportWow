from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(League)
admin.site.register(Coach)
admin.site.register(Country)
admin.site.register(Team)
admin.site.register(TeamCoach)
admin.site.register(TeamPlayer)
admin.site.register(City)
admin.site.register(Stadium)
admin.site.register(Match)