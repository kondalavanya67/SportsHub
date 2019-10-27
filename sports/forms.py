from django import forms
from sports.models import Sport, Tournaments


class FavoriteSports(forms.ModelForm):
    class Meta:
        model = Sport
        fields = ['name']


class TournamentRegistration(forms.ModelForm):
    class Meta:
        model = Tournaments
        fields = ['name', 'description', 'location', 'start_date', 'end_date']
