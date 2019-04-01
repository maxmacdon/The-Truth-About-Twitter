import pandas as pd
import os

results_path = 'results/'

# Read in all csv files in results directory and add them to dataframe
final_df = pd.DataFrame()
for file in os.listdir(results_path):
    df = pd.read_csv(results_path + file)
    final_df = final_df.append(df, sort=False)

# Display each model types top 5 results ordered by harmonic mean
for model in final_df.type.unique():
    df = final_df.loc[final_df['type'] == model]
    print('Model type: ' + model)
    df = df[['name', 'exp', 'recall', 'precision', 'f1', 'harmonic_mean']]
    df = df.sort_values('harmonic_mean', ascending=False)
    print(df.head(n=5))

