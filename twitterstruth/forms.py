from django import forms


# Simple form for user to enter twitter username
class UsernameForm(forms.Form):
    username = forms.CharField(label='Please enter a Twitter username', max_length=16)
