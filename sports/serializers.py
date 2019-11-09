from sports.models import Tournaments, TournamentJoin
from rest_framework import serializers


class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournaments
        fields = ['pk', 'name', 'description', 'location', 'start_date', 'end_date']


class JoinTournamentSerializer(serializers.ModelSerializer):
    # tournament = serializers.SerializerMethodField(method_name='get_tournament')
    # tournament = TournamentSerializer(read_only=True, many=True)

    class Meta:
        model = TournamentJoin
        fields = ['name', 'mail', 'tournament', 'phoneNumber']

    # def get_tournament(self, obj):
    #     return obj.tournament.name
