import json
import twython
import os
import pickle
from django.shortcuts import render
from django.conf import settings
from .forms import UsernameForm
import numpy as np


# Source: https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python
# Date Accessed: Jan 2019
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
# End Code Used


def home(request):
    if request.method == 'POST':
        form = UsernameForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']

            # Read in Twitter dev credentials
            file_name = os.path.join(settings.BASE_DIR, 'twitterstruth\\credentials\\twitter_credentials.json')
            with open(file_name, "r") as file:
                creds = json.load(file)

            try:
                # Setup Authorisation to Twitter API
                twitter = twython.Twython(creds['CONSUMER_KEY'], access_token=creds['ACCESS_TOKEN'])

                tweets = twitter.get_user_timeline(screen_name=username)
                user = twitter.show_user(screen_name=username)

                if user['verified']:
                    result, img = 'Real (Verified)', 'static/gifs/diamond.gif'
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

                    # Check user's properties to create instance for model
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

                    fake_followers = pickle.load(open(os.path.join(settings.BASE_DIR,
                                                      'twitterstruth\\ml_models\\fake_followers.sav'), 'rb'))
                    # Check ff then trad then social and only then return real
                    if fake_followers.predict(instance) == 0:
                        traditional_spam = pickle.load(open(os.path.join(settings.BASE_DIR,
                                                            'twitterstruth\\ml_models\\traditional_spam.sav'), 'rb'))
                        if traditional_spam.predict(instance) == 0:
                            social_spam = pickle.load(open(os.path.join(settings.BASE_DIR,
                                                           'twitterstruth\\ml_models\\social_spam.sav'), 'rb'))
                            if social_spam.predict(instance) == 0:
                                result, img = 'Real', 'static/gifs/social.gif'
                            else:
                                result, img = 'Social Spambot', 'static/gifs/snoop.gif'
                        else:
                            result, img = 'Traditional Spambot', 'static/gifs/traditional.gif'
                    else:
                        result, img = 'Fake Follower', 'static/gifs/follower.gif'
            except twython.TwythonError:
                result, img = 'No user found', 'static/gifs/wasted.gif'
            check = True
    else:
        check = False
        result, img, username = '', '', ''
        form = UsernameForm()
    return render(request, 'twitterstruth/home.html', {'form': form, 'result': result, 'img': img,
                                                       'check': check, 'username': username})


def about(request):
    return render(request, 'twitterstruth/about.html')
