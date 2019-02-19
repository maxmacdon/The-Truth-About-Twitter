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
            api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
            tweets = api.user_timeline(username)
            # End code used
            user = api.get_user(username, include_entities=1)
            print(user)
            # print('Screen name: ' + user['screen_name'])
            # print('Description: ' + user['description'])
            # print('Geo-located: ' + str(user['geo_enabled']))
            # print('Followers: ' + str(user['followers_count']))
            # print('Friends: ' + str(user['friends_count']))
            # print('Language: ' + user['lang'])
            # print('Total tweets: ' + str(user['statuses_count']))
            # print('Protected: ' + str(user['protected']))
            # print('Verified: ' + str(user['verified']))
            # print('Profile image: ' + user['profile_image_url'])
            # print('Default profile image: ' + str(user['default_profile_image']))
            # for tweet in tweets:
            #     print(tweet['text'])
            tweets_header = 'These are the 20 most recent tweets from ' + username
    else:
        form = UsernameForm()

    return render(request, 'index.html', {'form': form, 'tweets': tweets, 'tweets_header': tweets_header})


