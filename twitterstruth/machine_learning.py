import os
import django
import numpy as np
import random


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'The_Truth_about_Twitter.settings')
django.setup()


from twitterstruth.models import Account


def get_accounts(dum_features, dum_targets, account_type, sample_size):
    accounts = Account.objects.filter(account_type=account_type)
    random_accounts = random.sample(list(accounts), sample_size)

    for acc in random_accounts:
        dum_features.append([acc.default_profile_pic, acc.gt_1000_friends, acc.lt_30_friends, acc.never_tweeted,
                             acc.no_desc, acc.no_name, acc.not_geo_located, acc.three_friends_one_followers])

        if acc.real_account:
            dum_targets.append([0])
        else:
            dum_targets.append([1])

    return dum_features, dum_targets


features = []
targets = []

features, targets = get_accounts(features, targets, 1, 100)
features, targets = get_accounts(features, targets, 4, 100)

features = np.asarray(features)
np.random.shuffle(features)
targets = np.asarray(targets)
np.random.shuffle(targets)
