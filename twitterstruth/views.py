import json
import tweepy
import os
import pickle
from django.shortcuts import render
from django.conf import settings
from .forms import UsernameForm
import numpy as np

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            # j+1 instead of j since previous_row and current_row are one character longer than s2
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def home(request):
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
            if user['verified']:
                result = 'Real -> Verified'
            else:
                instance = []

                # Get levenshtein distance between tweets
                lev_distance = 300

                # Only if there is more then one entry in tweets proceed
                if tweets and len(tweets) != 1:
                    for tweet1 in tweets:
                        for tweet2 in tweets:
                            if str(tweet1['text']) != str(tweet2['text']):
                                tweet_distance = levenshtein(str(tweet1['text']), str(tweet2['text']))
                                if tweet_distance < lev_distance:
                                    lev_distance = tweet_distance

                if not user['screen_name']:
                    instance.append(1)
                else:
                    instance.append(0)

                if user['default_profile_image'] == 1.0:
                    instance.append(1)
                else:
                    instance.append(0)

                if user['geo_enabled'] != 1.0:
                    instance.append(1)
                else:
                    instance.append(0)

                if not user['description']:
                    instance.append(1)
                else:
                    instance.append(0)

                if user['friends_count'] < 30:
                    instance.append(1)
                    instance.append(0)
                elif user['friends_count'] > 1000:
                    instance.append(0)
                    instance.append(1)
                else:
                    instance.append(0)
                    instance.append(0)

                if user['statuses_count'] == 0:
                    instance.append(1)
                else:
                    instance.append(0)

                if user['friends_count'] > 3 * user['followers_count']:
                    instance.append(1)
                else:
                    instance.append(0)

                if user['statuses_count'] < 50:
                    instance.append(1)
                else:
                    instance.append(0)

                if lev_distance < 30:
                    instance.append(1)
                else:
                    instance.append(0)

                if user['lang'] != 'en':
                    instance.append(1)
                else:
                    instance.append(0)

                if user['friends_count'] > 50 * user['followers_count']:
                    instance.append(1)
                else:
                    instance.append(0)

                if user['friends_count'] > 100 * user['followers_count']:
                    instance.append(1)
                else:
                    instance.append(0)

                if 'www' in user['description'] or 'http' in user['description']:
                    instance.append(1)
                else:
                    instance.append(0)
                instance = np.asarray(instance)
                instance = instance.reshape(1, -1)

                social_spam = pickle.load(open(os.path.join(settings.BASE_DIR,
                                                            'twitterstruth\\ml_models\\social_spam.sav'), 'rb'))
                if social_spam.predict(instance) == 0:
                    traditional_spam = pickle.load(open(os.path.join(settings.BASE_DIR,
                                                                     'twitterstruth\\ml_models\\traditional_spam.sav'),
                                                        'rb'))
                    if traditional_spam.predict(instance) == 0:
                        fake_followers = pickle.load(open(os.path.join(settings.BASE_DIR,
                                                                       'twitterstruth\\ml_models\\fake_followers.sav'),
                                                          'rb'))
                        if fake_followers.predict(instance) == 0:
                            result = 'Real'
                        else:
                            result = 'Fake Follower'
                    else:
                        result = 'Traditional'
                else:
                    result = 'Social'

    else:
        result = ''
        form = UsernameForm()

    return render(request, 'twitterstruth/home.html', {'form': form, 'result': result})


def about(request):
    return render(request, 'twitterstruth/about.html')
