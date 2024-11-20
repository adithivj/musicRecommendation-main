import pandas as pd

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

song_dataset_df = pd.read_csv('../resources/FinalDataset/tracks_final_dataset.csv')

print(song_dataset_df.columns)

#print(song_dataset_df.shape)

song_dataset_df = song_dataset_df.drop_duplicates()

#print(song_dataset_df.shape)

#print(song_dataset_df.isnull().sum())

#print(song_dataset_df.dtypes)

#max of the values
#print(song_dataset_df.max(axis=0))


#print(song_dataset_df.min(axis=0))

# Analyse and understand the data attributs
#Top 20 popular artists in the dataset. This will help in testing




song_count_per_artist = song_dataset_df.groupby('artist1',as_index=False).agg({"id": "nunique"})
song_count_per_artist = song_count_per_artist.rename({'id': 'track_count_per_artist'}, axis=1)
song_count_per_artist = song_count_per_artist.sort_values(by=["track_count_per_artist"], ascending=False)
print(song_count_per_artist.head(10))

#References: https://pythonspot.com/matplotlib-bar-chart/

top_30_artists = song_count_per_artist.head(10)

top_30_artists = top_30_artists.sort_values(by=["track_count_per_artist"], ascending=True)
position_y = np.arange(10)
#track_count = np.arange(top_30_artists["track_count_per_artist"].all)

track_count =top_30_artists["track_count_per_artist"].to_numpy(dtype=str)
plt.bar(position_y, track_count, align='center', alpha=0.5)

plt.xticks(position_y, top_30_artists['artist1'].tolist())
plt.ylabel('Usage')
plt.title('Programming language usage')

plt.show()
#print()

