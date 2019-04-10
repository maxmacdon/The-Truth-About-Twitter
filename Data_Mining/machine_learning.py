import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold, StratifiedKFold
from sklearn.naive_bayes import BernoulliNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
from sklearn.metrics import confusion_matrix, f1_score, recall_score, precision_score
import psycopg2
from config import config


# Convert account details into features and targets
def create_features(accounts, acc):
    features = []
    targets = []

    for account in accounts:
        instance = []

        # Exp 1 Min features
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

        # Multi-class?
        if acc == 1:
            targets.append(account[10])
        else:
            # Is it marked as a real or fake account?
            if account[9]:
                targets.append(0)
            else:
                targets.append(1)

        # Exp 2 Maximum features
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

    return features, targets


def train_models(df, type, exp, acc):
    df['type'] = type
    df['exp'] = exp
    conn = None
    try:
        # Load db parameters and connect
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        sql = "SELECT name, default_profile_image, geo_enabled, description, friends_count, statuses_count, " \
              "followers_count, lev_distance, lang, real_account, account_type FROM account"

        # Do resampling if needed and only get required account types
        if acc == 0:
            cur.execute(sql)
            accounts = cur.fetchall()
            features_1, targets_1 = create_features(accounts, acc)

            cur.execute(sql + " WHERE account_type = " + str(acc))
            accounts = cur.fetchall()
            features_2, targets_2 = create_features(accounts, acc)
            features = features_1 + features_2
            targets = targets_1 + targets_2
        else:
            if acc == 1:
                cur.execute(sql)
            else:
                cur.execute(sql + " WHERE account_type in (1," + str(acc) + ")")
            accounts = cur.fetchall()
            features, targets = create_features(accounts, acc)
        cur.close()

        # Convert lists to NumPy arrays
        features = np.asarray(features)
        targets = np.asarray(targets)

        # Initialise classifiers and stratified and normal k-fold cross validation
        classifiers = [
            DecisionTreeClassifier(),
            BernoulliNB(),
            KNeighborsClassifier(n_neighbors=10, algorithm='auto'),
            LinearSVC(dual=False)]
        kf = KFold(n_splits=10, shuffle=True)
        skf = StratifiedKFold(n_splits=10)

        # Train classifier using stratified or normal k-fold cross validation and save the best performing classifier
        for train, test in skf.split(features, targets):# kf.split(features)
            for index in range(4):
                classifiers[index].fit(features[train], targets[train])
                results = classifiers[index].predict(features[test])

                # Get accuracy scores depending if binary or multiclass
                if acc != 1:
                    cm = confusion_matrix(targets[test], results)
                    recall = recall_score(targets[test], results)
                    precision = precision_score(targets[test], results)
                    f1 = f1_score(targets[test], results)
                    recall_list = recall_score(targets[test], results, average=None)
                else:
                    cm = confusion_matrix(targets[test], results, labels=[1, 2, 3, 4])
                    recall = recall_score(targets[test], results, average='macro', labels=np.unique(results))
                    precision = precision_score(targets[test], results, average='macro', labels=np.unique(results))
                    f1 = f1_score(targets[test], results, average='macro', labels=np.unique(results))
                    recall_list = recall_score(targets[test], results, average=None, labels=np.unique(results))

                # Add confusion matrix elements to dataframe
                cm_index = 3
                for row in cm:
                    for col in row:
                        df.iloc[index, cm_index] += col
                        cm_index += 1

                df.iloc[index, cm_index] += recall
                df.iloc[index, cm_index + 1] += precision
                df.iloc[index, cm_index + 2] += f1

                # Compute average class accuracy(harmonic mean)
                harmonic_mean = 0
                for rec in recall_list:
                    if rec != 0:
                        harmonic_mean += 1 / rec
                harmonic_mean = 1 / ((1 / len(recall_list)) * harmonic_mean)
                df.iloc[index, cm_index + 3] += harmonic_mean

        # Get average over all the folds
        df.recall = df.recall.div(10)
        df.precision = df.precision.div(10)
        df.f1 = df.f1.div(10)
        df.harmonic_mean = df.harmonic_mean.div(10)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return df


# Dataframe for binary classifiers
d_binary = {'name': ['dt', 'nbb', 'knn', 'svm'],
            'type': ['', '', '', ''],
            'exp': ['', '', '', ''],
            'cm_00': [0, 0, 0, 0], 'cm_01': [0, 0, 0, 0],
            'cm_10': [0, 0, 0, 0], 'cm_11': [0, 0, 0, 0],
            'recall': [0, 0, 0, 0],
            'precision': [0, 0, 0, 0],
            'f1': [0, 0, 0, 0],
            'harmonic_mean': [0, 0, 0, 0]}
# Dataframe for multiclass classifiers
d_multi = {'name': ['dt', 'nbb', 'knn', 'svm'],
           'type': ['', '', '', ''],
           'exp': ['', '', '', ''],
           'cm_00': [0, 0, 0, 0], 'cm_01': [0, 0, 0, 0], 'cm_02': [0, 0, 0, 0], 'cm_03': [0, 0, 0, 0],
           'cm_10': [0, 0, 0, 0], 'cm_11': [0, 0, 0, 0], 'cm_12': [0, 0, 0, 0], 'cm_13': [0, 0, 0, 0],
           'cm_20': [0, 0, 0, 0], 'cm_21': [0, 0, 0, 0], 'cm_22': [0, 0, 0, 0], 'cm_23': [0, 0, 0, 0],
           'cm_30': [0, 0, 0, 0], 'cm_31': [0, 0, 0, 0], 'cm_32': [0, 0, 0, 0], 'cm_33': [0, 0, 0, 0],
           'recall': [0, 0, 0, 0],
           'precision': [0, 0, 0, 0],
           'f1': [0, 0, 0, 0],
           'harmonic_mean': [0, 0, 0, 0]}

final_df = pd.DataFrame()
final_df = final_df.append(train_models(pd.DataFrame(data=d_multi), 'r v ff v t v s', 'resamp_4', 1), sort=False)
final_df = final_df.append(train_models(pd.DataFrame(data=d_binary), 'r v f', 'resamp_4', 0), sort=False)
final_df = final_df.append(train_models(pd.DataFrame(data=d_binary), 'r v ff', 'resamp_4', 2), sort=False)
final_df = final_df.append(train_models(pd.DataFrame(data=d_binary), 'r v s', 'resamp_4', 4), sort=False)
final_df = final_df.append(train_models(pd.DataFrame(data=d_binary), 'r v t', 'resamp_4', 3), sort=False)

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(final_df)

results_file = 'results/exp4_binary_multi_sep_resampling.csv'
final_df.to_csv(results_file, header=True)
