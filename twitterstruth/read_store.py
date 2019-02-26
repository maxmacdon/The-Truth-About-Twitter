import pandas as pd
import os
import django

# Ensure file when run separately can access models and settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'The_Truth_about_Twitter.settings')
django.setup()
from twitterstruth.models import Account
from django.conf import settings


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


def read_in_csv(directory, account_type):
    # Read in users and tweets CSV files
    BASE_DIR = getattr(settings, "BASE_DIR")

    try:
        users_file = os.path.join(BASE_DIR, 'data/' + directory + '/users.csv')
        users = pd.read_csv(users_file)
        users = users.fillna(-1)

        if account_type == 1:
            real_account = True
        else:
            real_account = False

        # Perform data transformation
        for user in users.itertuples():
            # Get levenshtein distance between tweets
            lev_distance = 300
            tweets_text = []
            user_id = getattr(user, 'id')
            try:
                count = 0
                tweets_file = 'data/' + directory + '/tweets.csv'

                for tweets in pd.read_csv(tweets_file, chunksize=2000000, usecols=['text', 'user_id']):
                    tweets = tweets.fillna(value={'text': '', 'user_id': -1})
                    tweets = tweets[tweets['user_id'] == user_id]

                    for tweet in tweets.itertuples():
                        if count == 20:
                            break
                        else:
                            tweet_user_id = int(getattr(tweet, 'user_id'))
                            if user_id == tweet_user_id:
                                tweets_text.append(getattr(tweet, 'text'))
                                count += 1
            except FileNotFoundError:
                pass

            if tweets_text and len(tweets_text) != 1:
                for text1 in tweets_text:
                    for text2 in tweets_text:
                        if str(text1) != str(text2):
                            tweet_distance = levenshtein(str(text1), str(text2))
                            if tweet_distance < lev_distance:
                                lev_distance = tweet_distance

            # Enter data into database
            Account.objects.create(id=getattr(user, 'id'), real_account=real_account, account_type=account_type,
               name=getattr(user, 'name'), screen_name=getattr(user, 'screen_name'),
               statuses_count=getattr(user, 'statuses_count'), followers_count=getattr(user, 'followers_count'),
               friends_count=getattr(user, 'friends_count'), favourites_count=getattr(user, 'favourites_count'),
               listed_count=getattr(user, 'listed_count'), url=getattr(user, 'url'), lang=getattr(user, 'lang'),
               time_zone=getattr(user, 'time_zone'), default_profile_image=getattr(user, 'default_profile_image'),
               default_profile=getattr(user, 'default_profile'), location=getattr(user, 'location'),
               geo_enabled=getattr(user, 'geo_enabled'), profile_image_url=getattr(user, 'profile_image_url'),
               profile_image_url_https=getattr(user, 'profile_image_url_https'),
               profile_banner_url=getattr(user, 'profile_banner_url'), description=getattr(user, 'description'),
               profile_use_background_image=getattr(user, 'profile_use_background_image'),
               profile_background_image_url=getattr(user, 'profile_background_image_url'),
               profile_background_image_url_https=getattr(user, 'profile_background_image_url_https'),
               profile_background_tile=getattr(user, 'profile_background_tile'), utc_offset=getattr(user, 'utc_offset'),
               protected=getattr(user, 'protected'), verified=getattr(user, 'verified'), lev_distance=lev_distance)
    except FileNotFoundError:
        return


def read_in_all_data():
    Account.objects.all().delete()
    read_in_csv('genuine_accounts', 1)
    read_in_csv('fake_followers', 2)
    read_in_csv('social_spambots_1', 3)
    read_in_csv('social_spambots_2', 3)
    read_in_csv('social_spambots_3', 3)
    read_in_csv('traditional_spambots_1', 4)
    read_in_csv('traditional_spambots_2', 4)
    read_in_csv('traditional_spambots_3', 4)
    read_in_csv('traditional_spambots_4', 4)


read_in_all_data()
