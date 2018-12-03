import os
import django
import numpy as np
import random
from sklearn.model_selection import KFold, cross_val_score
from sklearn.naive_bayes import BernoulliNB


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'The_Truth_about_Twitter.settings')
django.setup()
from twitterstruth.models import Account


def get_accounts(dum_features, dum_targets, account_type, sample_size):
    accounts = Account.objects.filter(account_type=account_type)
    random_accounts = random.sample(list(accounts), sample_size)

    for acc in random_accounts:
        dum_features.append([acc.default_profile_pic, acc.gt_1000_friends,
                             acc.lt_30_friends, acc.never_tweeted,
                             acc.no_desc, acc.no_name, acc.not_geo_located,
                             acc.three_friends_one_followers])

        if acc.real_account:
            dum_targets.append(0)
        else:
            dum_targets.append(1)

    return dum_features, dum_targets


features = []
targets = []

features, targets = get_accounts(features, targets, 1, 1000)
features, targets = get_accounts(features, targets, 4, 1000)

features = np.asarray(features)
targets = np.asarray(targets)

kf = KFold(n_splits=10, shuffle=True)
clf = BernoulliNB()

print('Data comprises of 2000 shuffled accounts:\n'
      '    1000 random Genuine accounts\n'
      '    1000 random Traditional accounts\n'
      'K-fold Cross validation used with k = 10\n'
      'Classifier: Naive Bayes with Bernoulli distribution\n'
      'Mean of the partition scores for each run:\n')
for index in range(5):
    scores = cross_val_score(estimator=clf, X=features, y=targets, cv=kf)
    print('    Run ' + str(index) + ': ' + str(np.mean(scores)))
