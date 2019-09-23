from django import forms
from sports.models import Sport


class FavoriteSports(forms.ModelForm):
    class Meta:
        model = Sport
        fields = ['name']
