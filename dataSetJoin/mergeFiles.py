import pandas as pd
import glob
import os

files = os.path.join("/Users/pk/Learn/CSE-6242/Project/SourceCode/project1/CSE6242-project-team-16/resources/FinalDataset1/", "tracks_final_dataset*.csv")

files = glob.glob(files)

print("Resultant CSV after joining all CSV files at a particular location...");

# joining files with concat and read_csv
songs_dataset = pd.concat(map(pd.read_csv, files), ignore_index=True)

print(songs_dataset.shape)

print(songs_dataset.columns)

songs_dataset = songs_dataset.drop(["Unnamed: 0","Unnamed: 0.1","Unnamed: 0.1.1"], axis=1)

print(songs_dataset.columns)


songs_dataset.to_csv('../resources/FinalDataset1/tracks_final_dataset.csv')