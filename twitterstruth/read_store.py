import pandas as pd
import os


def read_in(directory, ac_type):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    users_file = os.path.join(BASE_DIR, 'data\\' + directory + '\\users.csv')
    # tweets_file = os.path.join(BASE_DIR, 'data\\genuine_accounts\\tweets.csv')

    users = pd.read_csv(users_file)
    users = users.fillna('')

    # tweets = pd.read_csv(tweets_file)

    account_type = ac_type
    #Data Preperation
    for row in users.itertuples():
        id = getattr(row, 'id')
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

        print(id, account_type, default_prof_pic, no_name, no_desc, lt_30_friends, gt_1000_friends,
              no_geo_location, three_friends_one_follower, never_tweeted)

read_in('genuine_accounts', 1)
read_in('fake_followers', 2)
read_in('social_spambots_1', 3)
read_in('social_spambots_2', 3)
read_in('social_spambots_3', 3)
read_in('traditional_spambots_1', 4)
read_in('traditional_spambots_2', 4)
read_in('traditional_spambots_3', 4)
read_in('traditional_spambots_4', 4)
