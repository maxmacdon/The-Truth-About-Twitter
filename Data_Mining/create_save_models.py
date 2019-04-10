import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import KFold
from sklearn.metrics import recall_score
import psycopg2
import json
from config import config


# Convert account details into features and targets
def create_features(accounts):
    features = []
    targets = []

    for account in accounts:
        instance = []

        # Is there no name?
        if not account[0]:
            instance.append(1)
        else:
            instance.append(0)

        # Is the default profile image being used
        if account[1] == 1.0:
            instance.append(1)
        else:
            instance.append(0)

        # Is geo-location disabled?
        if account[2] != 1.0:
            instance.append(1)
        else:
            instance.append(0)

        # Is there no account description?
        if not account[3]:
            instance.append(1)
        else:
            instance.append(0)

        # Is friends count < 30?
        if account[4] < 30:
            instance.append(1)
            instance.append(0)
        # Or > 1000?
        elif account[4] > 1000:
            instance.append(0)
            instance.append(1)
        else:
            instance.append(0)
            instance.append(0)

        # Have they tweeted before?
        if account[5] == 0:
            instance.append(1)
        else:
            instance.append(0)

        # Is friends to followers ratio 3:1?
        if account[4] >= 3 * account[6]:
            instance.append(1)
        else:
            instance.append(0)

        # Have they tweeted < 50 times?
        if account[5] < 50:
            instance.append(1)
        else:
            instance.append(0)

        # Is levenstien distance between tweets < 30?
        if account[7] < 30:
            instance.append(1)
        else:
            instance.append(0)

        # Is the language not set to english?
        if account[8] != 'en':
            instance.append(1)
        else:
            instance.append(0)

        # Is friends to followers ratio 50:1?
        if account[4] >= 50 * account[6]:
            instance.append(1)
        else:
            instance.append(0)

        # Is friends to followers ratio 100:1?
        if account[4] >= 100 * account[6]:
            instance.append(1)
        else:
            instance.append(0)

        # Is there a link in the description
        if 'www' in account[3] or 'http' in account[3]:
            instance.append(1)
        else:
            instance.append(0)
        features.append(instance)

        # Is it marked as a real or fake account?
        if account[9]:
            targets.append(0)
        else:
            targets.append(1)

    return features, targets


def train_models(acc, filepath):
    conn = None
    try:
        # Load db parameters and connect
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        # Retrieve specified accounts
        cur.execute("SELECT name, default_profile_image, geo_enabled, description, friends_count, statuses_count,"
                    "followers_count, lev_distance, lang, real_account"
                    " FROM account WHERE account_type in (1," + str(acc) + ")")
        accounts = cur.fetchall()
        features, targets = create_features(accounts)

        cur.close()

        # Convert lists to NumPy arrays
        features = np.asarray(features)
        targets = np.asarray(targets)

        # Initialise classifiers and k-fold cross validation
        clf = DecisionTreeClassifier()
        kf = KFold(n_splits=10, shuffle=True)
        best_hm, best_train, best_targets = 0, [], []

        # Train classifier using K fold cross validation and save the best performing classifier
        for train, test in kf.split(features):
            clf.fit(features[train], targets[train])
            recall_list = recall_score(targets[test], clf.predict(features[test]), average=None)
            harmonic_mean = 1 / ((1 / 2) * ((1 / recall_list[0]) + (1 / recall_list[0])))

            if harmonic_mean > best_hm:
                best_hm = harmonic_mean
                best_train = features[train]
                best_targets = targets[train]

        # Source: https://stackabuse.com/scikit-learn-save-and-restore-models/
        # Date Accessed: April 2019
        # A method for saving object data to JSON file
        dict_ = {}
        dict_['x_train'] = best_train.tolist() if best_train is not None else 'None'
        dict_['y_train'] = best_targets.tolist() if best_targets is not None else 'None'

        # Create json and save to file
        json_txt = json.dumps(dict_, indent=4)
        with open(filepath, 'w') as file:
            file.write(json_txt)
        # End Code Used
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


train_models(2, '../The_Truth_about_Twitter/twitterstruth/ml_models/fake_followers.json')
train_models(3, '../The_Truth_about_Twitter/twitterstruth/ml_models/traditional_spam.json')
train_models(4, '../The_Truth_about_Twitter/twitterstruth/ml_models/social_spam.json')
