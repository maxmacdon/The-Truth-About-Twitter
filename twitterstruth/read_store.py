import pandas as pd
import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'The_Truth_about_Twitter.settings')
django.setup()


from twitterstruth.models import Account
from django.conf import settings


def read_in_csv(directory, account_type):
    BASE_DIR = getattr(settings, "BASE_DIR")
    users_file = os.path.join(BASE_DIR, 'data/' + directory + '/users.csv')
    # tweets_file = os.path.join(BASE_DIR, 'data\\genuine_accounts\\tweets.csv')

    users = pd.read_csv(users_file)
    users = users.fillna('')

    # tweets = pd.read_csv(tweets_file)

    # Data Preperation
    if account_type == 1:
        real_account = True
    else:
        real_account = False

    for row in users.itertuples():
        account_id = getattr(row, 'id')
        friends = getattr(row, 'friends_count')
        if not getattr(row, 'name'):
            no_name = 1
        else:
            no_name = 0
        if getattr(row, 'default_profile_image') == 1.0:
            default_prof_pic = 1
        else:
            default_prof_pic = 0
        if getattr(row, 'geo_enabled') != 1.0:
            no_geo_location = 1
        else:
            no_geo_location = 0
        if not getattr(row, 'description'):
            no_desc = 1
        else:
            no_desc = 0
        if friends < 30:
            lt_30_friends = 1
            gt_1000_friends = 0
        elif friends > 1000:
            lt_30_friends = 0
            gt_1000_friends = 1
        else:
            lt_30_friends = 0
            gt_1000_friends = 0
        if getattr(row, 'statuses_count') == 0:
            never_tweeted = 1
        else:
            never_tweeted = 0
        if friends > 3 * getattr(row, 'followers_count'):
            three_friends_one_follower = 1
        else:
            three_friends_one_follower = 0

        Account.objects.create(id=account_id, real_account=real_account, account_type=account_type,
                               default_profile_pic=default_prof_pic, no_name=no_name, no_desc=no_desc,
                               lt_30_friends=lt_30_friends, gt_1000_friends=gt_1000_friends,
                               not_geo_located=no_geo_location, never_tweeted=never_tweeted,
                               three_friends_one_followers=three_friends_one_follower)


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
