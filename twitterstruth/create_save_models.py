import os
import django
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import KFold
from sklearn.metrics import recall_score
import pickle

# Ensure file when run separately can access models and settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'The_Truth_about_Twitter.settings')
django.setup()
from twitterstruth.models import Account
from django.db.models import Q
from django.conf import settings


# Convert account details into features and targets
def create_features(accounts):
    features = []
    targets = []

    for account in accounts:
        instance = []

        if not account.name:
            instance.append(1)
        else:
            instance.append(0)

        if account.default_profile_image == 1.0:
            instance.append(1)
        else:
            instance.append(0)

        if account.geo_enabled != 1.0:
            instance.append(1)
        else:
            instance.append(0)

        if not account.description:
            instance.append(1)
        else:
            instance.append(0)

        if account.friends_count < 30:
            instance.append(1)
            instance.append(0)
        elif account.friends_count > 1000:
            instance.append(0)
            instance.append(1)
        else:
            instance.append(0)
            instance.append(0)

        if account.statuses_count == 0:
            instance.append(1)
        else:
            instance.append(0)

        if account.friends_count > 3 * account.followers_count:
            instance.append(1)
        else:
            instance.append(0)

        if account.statuses_count < 50:
            instance.append(1)
        else:
            instance.append(0)

        if account.lev_distance < 30:
            instance.append(1)
        else:
            instance.append(0)

        if account.lang != 'en':
            instance.append(1)
        else:
            instance.append(0)

        if account.friends_count > 50 * account.followers_count:
            instance.append(1)
        else:
            instance.append(0)

        if account.friends_count > 100 * account.followers_count:
            instance.append(1)
        else:
            instance.append(0)

        if 'www' in account.description or 'http' in account.description:
            instance.append(1)
        else:
            instance.append(0)
        features.append(instance)

        if account.real_account:
            targets.append(0)
        else:
            targets.append(1)

    return features, targets


def train_models(acc, filename):
    accounts = Account.objects.filter(Q(account_type=1) | Q(account_type=acc))

    features, targets = create_features(accounts)

    # Convert lists to NumPy arrays
    features = np.asarray(features)
    targets = np.asarray(targets)

    # Initialise classifiers and k-fold cross validation
    clf = DecisionTreeClassifier()
    kf = KFold(n_splits=10, shuffle=True)
    best_hm = 0

    # Train classifier using K fold cross validation and save the best performing classifier
    for train, test in kf.split(features):
        clf.fit(features[train], targets[train])
        recall_list = recall_score(targets[test], clf.predict(features[test]), average=None)
        harmonic_mean = 1 / ((1 / 2) * ((1 / recall_list[0]) + (1 / recall_list[0])))

        if harmonic_mean > best_hm:
            best_hm = harmonic_mean
            final_clf = clf

    # Save classifier to file
    BASE_DIR = getattr(settings, "BASE_DIR")
    filepath = os.path.join(BASE_DIR, filename)
    pickle.dump(final_clf, open(filepath, 'wb'))


train_models(2, 'twitterstruth/ml_models/fake_followers.sav')
train_models(3, 'twitterstruth/ml_models/traditional_spam.sav')
train_models(4, 'twitterstruth/ml_models/social_spam.sav')
