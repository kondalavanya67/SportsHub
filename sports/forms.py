from django import forms
from sports.models import Sport_Info, Tournaments, CoachingCenters, TournamentJoin


class FavoriteSports(forms.ModelForm):
    class Meta:
        model = Sport_Info
        fields = ['name']


class TournamentRegistration(forms.ModelForm):
    class Meta:
        model = Tournaments
        fields = ['name', 'description', 'location', 'start_date', 'end_date']


class CoachingCenterRegistration(forms.ModelForm):
    class Meta:
        model = CoachingCenters
        fields = ['name', 'description', 'address']


class TournamentJoinForm(forms.ModelForm):
    class Meta:
        model = TournamentJoin
        fields = ['name', 'mail', 'phoneNumber']
