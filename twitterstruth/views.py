import json
import tweepy
import os
from django.shortcuts import render
from django.conf import settings
from .forms import UsernameForm


def index(request):
    tweets = None
    tweets_header = ''

    if request.method == 'POST':
        form = UsernameForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']

            # Read in Twitter dev credentials
            file_name = os.path.join(settings.BASE_DIR, 'twitterstruth\\credentials\\twitter_credentials.json')
            with open(file_name, "r") as file:
                creds = json.load(file)

            # Source https://tweepy.readthedocs.io/en/v3.6.0/getting_started.html
            # Date Accessed: October 2018
            auth = tweepy.OAuthHandler(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])
            auth.set_access_token(creds['ACCESS_TOKEN'], creds['ACCESS_SECRET'])

            # Retrieve 20 most recent tweets from Twitter API of account:username
            api = tweepy.API(auth)
            tweets = api.user_timeline(username)
            tweets_header = 'These are the 20 most recent tweets from ' + username
    else:
        form = UsernameForm()

    return render(request, 'index.html', {'form': form, 'tweets': tweets, 'tweets_header': tweets_header})


