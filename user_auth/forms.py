from django import forms
from django.contrib.auth.models import User

from user_auth.models import Profile


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password1 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("Username is already taken")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email is already registered")
        return email

    def clean_password1(self):
        password = self.cleaned_data.get('password')
        password1 = self.cleaned_data.get('password1')
        if password != password1:
            raise forms.ValidationError("Passwords do not match!")
        return password1


class UserProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['location']
