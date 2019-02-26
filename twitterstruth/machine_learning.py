import os
import django
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold
from sklearn.naive_bayes import BernoulliNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
from sklearn.metrics import confusion_matrix, f1_score, recall_score, precision_score

# Ensure file when run separately can access models and settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'The_Truth_about_Twitter.settings')
django.setup()
from twitterstruth.models import Account
from django.conf import settings


features = []
targets = []

for account in Account.objects.all():
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
    features.append(instance)
    # targets.append(account.account_type)
    if account.real_account:
        targets.append(0)
    else:
        targets.append(1)

# Convert lists to NumPy arrays
features = np.asarray(features)
targets = np.asarray(targets)

# Initialise classifiers and k-fold cross validation
classifiers = [
    DecisionTreeClassifier(),
    BernoulliNB(),
    KNeighborsClassifier(),
    LinearSVC()]
kf = KFold(n_splits=10, shuffle=True)

d = {'name': ['dt', 'nbb', 'knn', 'svm'],
     'cm_00': [0, 0, 0, 0], 'cm_01': [0, 0, 0, 0], 'cm_10': [0, 0, 0, 0], 'cm_11': [0, 0, 0, 0],
     # 'cm_00': [0, 0, 0, 0], 'cm_01': [0, 0, 0, 0], 'cm_02': [0, 0, 0, 0], 'cm_03': [0, 0, 0, 0],
     # 'cm_10': [0, 0, 0, 0], 'cm_11': [0, 0, 0, 0], 'cm_12': [0, 0, 0, 0], 'cm_13': [0, 0, 0, 0],
     # 'cm_20': [0, 0, 0, 0], 'cm_21': [0, 0, 0, 0], 'cm_22': [0, 0, 0, 0], 'cm_23': [0, 0, 0, 0],
     # 'cm_30': [0, 0, 0, 0], 'cm_31': [0, 0, 0, 0], 'cm_32': [0, 0, 0, 0], 'cm_33': [0, 0, 0, 0],
     'recall': [0, 0, 0, 0],
     'precision': [0, 0, 0, 0],
     'f1': [0, 0, 0, 0],
     'harmonic_mean': [0, 0, 0, 0]}
df = pd.DataFrame(data=d)



# Train classifier using K fold cross validation and save the best performing classifier
for train, test in kf.split(features):
    for index in range(4):
        classifiers[index].fit(features[train], targets[train])
        results = classifiers[index].predict(features[test])

        cm = confusion_matrix(targets[test], results)#, labels=[1, 2, 3, 4])

        cm_index = 1
        for row in cm:
            for col in row:
                df.iloc[index, cm_index] += col
                cm_index += 1

        recall = recall_score(targets[test], results, average='binary')#, labels=np.unique(results))
        df.iloc[index, cm_index] += recall
        precision = precision_score(targets[test], results, average='binary')#, labels=np.unique(results))
        df.iloc[index, cm_index + 1] += precision
        f1 = f1_score(targets[test], results, average='binary')#, labels=np.unique(results))
        df.iloc[index, cm_index + 2] += f1

        recall_list = recall_score(targets[test], results, average=None)#, labels=np.unique(results))
        harmonic_mean = 0
        for rec in recall_list:
            if rec != 0:
                harmonic_mean += 1 / rec
        harmonic_mean = 1 / ((1 / len(recall_list)) * harmonic_mean)
        df.iloc[index, cm_index + 4] += harmonic_mean

df.recall = df.recall.div(10)
df.precision = df.precision.div(10)
df.f1 = df.f1.div(10)
df.f1_2 = df.f1_2.div(10)
df.harmonic_mean = df.harmonic_mean.div(10)

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(df)

# BASE_DIR = getattr(settings, "BASE_DIR")
# results_file = os.path.join(BASE_DIR, 'data/results/exp1_binary_few.csv')

# exp2_binary_all, exp3_binary_stratifying, exp4_binary_resampling, exp5_binary_parameters
# exp1_multi_few, exp2_multi_all, exp3_multi_stratifying, exp4_multi_resampling, exp5_multi_parameters
# exp1_separate_few, exp2_separate_all, exp3_separate_stratifying, exp4_separate_resampling, exp5_separate_parameters

# df.to_csv(results_file, header=False)