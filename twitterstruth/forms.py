from django import forms


class HandleForm(forms.Form):
    username = forms.CharField(label='Please enter a Twitter handle', max_length=16)