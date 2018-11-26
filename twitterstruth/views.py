from django.shortcuts import render
from django.conf import settings
from .forms import HandleForm
import json
import tweepy
import os


def index(request):
    tweets = None
    if request.method == 'POST':
        form = HandleForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']

            file_name = os.path.join(settings.BASE_DIR, 'twitterstruth\\credentials\\twitter_credentials.json')
            with open(file_name, "r") as file:
                creds = json.load(file)

            auth = tweepy.OAuthHandler(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])
            auth.set_access_token(creds['ACCESS_TOKEN'], creds['ACCESS_SECRET'])

            api = tweepy.API(auth)
            tweets = api.user_timeline(username)
    else:
        form = HandleForm()

    return render(request, 'index.html', {'form': form, 'tweets': tweets})


