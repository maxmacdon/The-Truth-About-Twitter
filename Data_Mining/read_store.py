import pandas as pd
import psycopg2
from config import config


# Source: https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python
# Date Accessed: Jan 2019
# Compute the levenshtein distance between 2 strings, taken from 2nd Year assignment
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


# Read in users and tweets CSV files
def read_in_csv(directory, account_type):
    conn = None
    sql = """INSERT INTO account(id, real_account, account_type, name, screen_name, statuses_count,
                            followers_count, friends_count, favourites_count, listed_count, url, lang, time_zone,
                            default_profile_image, default_profile, location, geo_enabled, 
                            profile_image_url, profile_image_url_https,
                            profile_banner_url, description, profile_use_background_image, profile_background_image_url,
                            profile_background_image_url_https, profile_background_tile, utc_offset, protected,
                            verified, lev_distance)
                            VALUES(%s);"""
    try:
        params = config()
        conn = psycopg2.connect(**params)
        users_file = 'data/' + directory + '/users.csv'
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

            # Only if there is more then one entry in tweets_text proceed
            if tweets_text and len(tweets_text) != 1:
                for text1 in tweets_text:
                    for text2 in tweets_text:
                        if str(text1) != str(text2):
                            tweet_distance = levenshtein(str(text1), str(text2))
                            if tweet_distance < lev_distance:
                                lev_distance = tweet_distance

            # Enter data into database
            cur = conn.cursor()
            cur.execute(sql, (getattr(user, 'id'), real_account, account_type, getattr(user, 'name'),
                              getattr(user, 'screen_name'), getattr(user, 'statuses_count'),
                              getattr(user, 'followers_count'), getattr(user, 'friends_count'),
                              getattr(user, 'favourites_count'), getattr(user, 'listed_count'),
                              getattr(user, 'url'), getattr(user, 'lang'), getattr(user, 'time_zone'),
                              getattr(user, 'default_profile_image'), getattr(user, 'default_profile'),
                              getattr(user, 'location'), getattr(user, 'geo_enabled'),
                              getattr(user, 'profile_image_url'), getattr(user, 'profile_image_url_https'),
                              getattr(user, 'profile_banner_url'), getattr(user, 'description'),
                              getattr(user, 'profile_use_background_image'),
                              getattr(user, 'profile_background_image_url'),
                              getattr(user, 'profile_background_image_url_https'),
                              getattr(user, 'profile_background_tile'), getattr(user, 'utc_offset'),
                              getattr(user, 'protected'), getattr(user, 'verified'), lev_distance,))
            conn.commit()
            cur.close()
    except FileNotFoundError:
        return
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


read_in_csv('genuine_accounts', 1)
read_in_csv('fake_followers', 2)
read_in_csv('social_spambots_1', 3)
read_in_csv('social_spambots_2', 3)
read_in_csv('social_spambots_3', 3)
read_in_csv('traditional_spambots_1', 4)
read_in_csv('traditional_spambots_2', 4)
read_in_csv('traditional_spambots_3', 4)
read_in_csv('traditional_spambots_4', 4)
