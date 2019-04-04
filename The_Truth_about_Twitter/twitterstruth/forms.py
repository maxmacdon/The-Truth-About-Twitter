from django import forms


# Simple form for user to enter twitter username
class UsernameForm(forms.Form):
    username = forms.CharField(label='Please enter a Twitter handle to see if that '
                                     'account is real or a form of bot', max_length=16)
