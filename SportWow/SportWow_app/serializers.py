from rest_framework import serializers

from .models import *


class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = '__all__'
        depth = 0


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'
        depth = 1


class TeamCoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamCoach
        fields = '__all__'
        depth = 1


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'
        depth = 0


class StadiumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stadium
        fields = '__all__'
        depth = 0


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'
        depth = 1


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'email',
            'first_name',
            'last_name'
        )
        extra_kwargs = {'password':{'write_only':True}}
        depth = 0

    def save(self):
        user = User(email=self.validated_data['email'],
                    username=self.validated_data['username'],
                    first_name=self.validated_data['first_name'],
                    last_name=self.validated_data['last_name'])
        password = self.validated_data['password']
        user.set_password(password)
        user.save()
        return user


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'
        depth = 3


class OrderedTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedTicket
        fields = '__all__'
        depth = 4


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
        depth = 0