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
        labels = {
            'name': 'Name',
            'description': 'Description',
            'location': 'Location',
            'start_date': 'Start Date (mm/dd/yy)',
            'end_date': 'End Date (mm/dd/yy)',
        }


class CoachingCenterRegistration(forms.ModelForm):
    class Meta:
        model = CoachingCenters
        fields = ['name', 'description', 'street_name', 'area', 'state', 'phone_num', 'mail', 'pincode']
        labels = {
            'name': 'Name',
            'description': 'Description',
            'mail': 'E-mail',
            'street_name': 'Street name',
            'contact_details': 'Contact details',
            'area': 'Area',
            'state': 'State',
            'pincode': 'Pincode',
        }


class TournamentJoinForm(forms.ModelForm):
    class Meta:
        model = TournamentJoin
        fields = ['name', 'mail', 'phoneNumber']
        labels = {
            'name': 'Name',
            'mail': 'E-mail',
            'phoneNumber': 'Phone Number'
        }
