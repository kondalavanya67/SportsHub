from django import forms
from .models import Review


class writereview(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Write about product', 'rows': '4', 'cols': '50'}))

    class Meta:
        model = Review
        fields = ['content']
