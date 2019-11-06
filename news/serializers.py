from sports.models import Tournaments
from rest_framework import serializers


class TournamentSerializer(serializers.ModelSerializer):
    # user = serializers.SerializerMethodField(method_name='get_username')

    class Meta:
        model = Tournaments
        fields = '__all__'

    # def get_username(self, obj):
    #     return obj.user.username
