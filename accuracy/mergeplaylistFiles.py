import pandas as pd
import glob
import os

files = os.path.join("/Users/pk/Learn/CSE-6242/workspace/CSE6242-project-team-16/resources/FinalDataSet1/", "playlist_tracks_*.csv")

files = glob.glob(files)

print("Resultant CSV after joining all CSV files at a particular location...");

# joining files with concat and read_csv
playlist_track_dataset = pd.concat(map(pd.read_csv, files), ignore_index=True)

print(playlist_track_dataset.shape)

print(playlist_track_dataset.columns)

playlist_track_dataset = playlist_track_dataset.drop(["Unnamed: 0"], axis=1)

#print(songs_dataset.columns)


playlist_track_dataset.to_csv('../resources/output/playlist_tracks.csv')