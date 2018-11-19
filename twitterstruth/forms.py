from django import forms


class HandleForm(forms.Form):
    twitter_handle = forms.CharField(label='Please enter a Twitter handle', max_length=16)