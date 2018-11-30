from django import forms


class UsernameForm(forms.Form):
    username = forms.CharField(label='Please enter a Twitter username', max_length=16)
