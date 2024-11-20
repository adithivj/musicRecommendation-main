import numpy as np
import pandas as pd

df = pd.read_csv('/Users/pk/Learn/CSE-6242/workspace2/CSE6242-project-team-16/resources/FinalDataSet1/tracks_final_dataset_clustered_sample.csv')
print(df.size)

# chosen_idx = np.random.choice(45886995, replace=False, size=2000000)
# df_trimmed = df.iloc[chosen_idx]

df_trimmed = df.sample(n=500)

df_trimmed.to_csv('../resources/FinalDataset1/tracks_final_dataset_clustered_sample1.csv')