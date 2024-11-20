import pandas as pd
from prince import FAMD
import numpy as np
from sklearn.preprocessing import StandardScaler

from kmodes.kprototypes import KPrototypes
def key(x):
    if x == 0:
        return "A"
    elif x == 1:
        return "B"
    elif x == 2:
        return "C"
    elif x == 3:
        return "D"
    elif x == 4:
        return "E"
    elif x == 5:
        return "F"
    elif x == 6:
        return "G"
    elif x == 7:
        return "H"
    elif x == 8:
        return "I"
    elif x == 9:
        return "J"
    elif x == 10:
        return "K"
    else:
        return "L"


def mode(x):
    if x == 0:
        return "minor"
    if x == 1:
        return "major"
    else:
        print("here")


def genre(x):
    row =x
    row = row.replace("[", "")
    row = row.replace("]", "")
    row = row.replace("'", "")
    row_list = row.split(", ")
    row = row_list[0]
    return row


df = pd.read_csv("/Users/pk/Learn/CSE-6242/workspace/CSE6242-project-team-16/resources/FinalDataSet1/tracks_final_dataset_clustered.csv")

df = df[["danceability", "energy", "key", "loudness",  "mode", "speechiness","acousticness", "instrumentalness", "liveness", "valence", "tempo", "genres",'listeners','playcount']]

scaled_df = StandardScaler().fit_transform(df[["danceability", "energy","loudness","speechiness","acousticness", "instrumentalness", "liveness", "valence", "tempo",'listeners','playcount' ]])
df[["danceability", "energy","loudness","speechiness","acousticness", "instrumentalness", "liveness", "valence", "tempo",'listeners','playcount']] = scaled_df

df["key"] = df["key"].apply(lambda x: key(x))
df["mode"] = df["mode"].apply(lambda x: mode(x))
df["genre"] = df["genres"].apply(lambda x: genre(x))


df = df.drop("genres", axis=1)

print(df.dtypes)

df_array = df.values;

print(df.head())
df = df.dropna()

print(df_array)

kproto = KPrototypes(n_clusters=3, verbose=2,max_iter=1)
cluster = kproto.fit(df_array, categorical=[2,4,13])
print("here")
