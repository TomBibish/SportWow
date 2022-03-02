from django.db import models

# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)

    def __str__(self):
        return f"{self.name}"


class City(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)
    country = models.ForeignKey(Country, on_delete=models.RESTRICT)

    def __str__(self):
        return f"{self.name}, {self.country}"


class Stadium(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)
    city = models.ForeignKey(City, on_delete=models.RESTRICT)
    capacity = models.CharField(max_length=6, null=False, blank=False)

    def __str__(self):
        return f"{self.name}, {self.city}"


class League(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)
    country = models.ForeignKey(Country, on_delete=models.RESTRICT)

    def __str__(self):
        return f"{self.name}"


class Team(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)
    city = models.ForeignKey(City, on_delete=models.RESTRICT)
    country = models.ForeignKey(Country, on_delete=models.RESTRICT)
    stadium = models.ForeignKey(Stadium, on_delete=models.RESTRICT)
    picture_url = models.URLField(blank=True, null=True)
    league = models.ForeignKey(League, on_delete=models.RESTRICT)
    points = models.CharField(max_length=3, null=True, blank=True,default=0)

    def __str__(self):
        return f"{self.name}"


class Player(models.Model):
    first_name = models.CharField(max_length=128, null=False, blank=False)
    last_name = models.CharField(max_length=128, null=False, blank=False)
    birth_date = models.DateField()
    country = models.ForeignKey(Country, on_delete=models.RESTRICT)
    picture_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class TeamPlayer(models.Model):
    player = models.ForeignKey(Player, on_delete=models.RESTRICT)
    team = models.ForeignKey(Team, on_delete=models.RESTRICT)
    is_active = models.BooleanField()

    def __str__(self):
        return f"{self.player} from {self.team}"


class Coach(models.Model):
    first_name = models.CharField(max_length=128, null=False, blank=False)
    last_name = models.CharField(max_length=128, null=False, blank=False)
    is_active = models.BooleanField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class TeamCoach(models.Model):
    coach = models.ForeignKey(Coach, on_delete=models.RESTRICT)
    team = models.ForeignKey(Team, on_delete=models.RESTRICT)
    is_active = models.BooleanField()

    def __str__(self):
        return f"{self.coach} of {self.team}"

