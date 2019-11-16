from datetime import datetime

from django import forms
from sports.models import Sport_Info, Tournaments, CoachingCenters, TournamentJoin


class FavoriteSports(forms.ModelForm):
    class Meta:
        model = Sport_Info
        fields = ['name']


class TournamentRegistration(forms.ModelForm):
    class Meta:
        model = Tournaments
        fields = ['name', 'description', 'location', 'start_date', 'end_date', 'image']
        labels = {
            'name': 'Name',
            'description': 'Description',
            'location': 'Location',
            'start_date': 'Start Date (yy-mm-dd)',
            'end_date': 'End Date (yy-mm-dd)',
            'image': 'Upload Image'
        }


class CoachingCenterRegistration(forms.ModelForm):
    class Meta:
        model = CoachingCenters
        fields = ['name', 'description', 'street_name', 'area', 'state', 'phone_num', 'mail', 'pincode', 'image']
        labels = {
            'name': 'Name',
            'description': 'Description',
            'mail': 'E-mail',
            'street_name': 'Street name',
            'phone_num': 'Phone Number',
            'area': 'Area',
            'state': 'State',
            'pincode': 'Pincode',
            'image': 'Upload Image'
        }

    def clean_phone_num(self):
        phone_num = self.cleaned_data['phone_num']
        print(phone_num)
        if len(str(phone_num)) != 10:
            raise forms.ValidationError('Enter a valid phone number')
        return phone_num

    def clean_pincode(self):
        pincode = self.cleaned_data['pincode']
        print(pincode)
        if len(str(pincode)) != 6:
            raise forms.ValidationError('Enter a valid pincode')
        return pincode


class TournamentJoinForm(forms.ModelForm):
    class Meta:
        model = TournamentJoin
        fields = ['name', 'mail', 'phoneNumber']
        labels = {
            'name': 'Name',
            'mail': 'E-mail',
            'phoneNumber': 'Phone Number'
        }

    def clean_phoneNumber(self):
        phone_num = self.cleaned_data['phoneNumber']
        print(phone_num)
        length = len(str(phone_num))
        if phone_num is not None and length != 10:
            raise forms.ValidationError('Enter a valid phone number')
        return phone_num
