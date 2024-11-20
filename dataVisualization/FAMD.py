import pandas as pd
from prince import FAMD
import numpy as np

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


df = pd.read_csv("/Users/pk/Learn/CSE-6242/workspace/CSE6242-project-team-16/resources/FinalDataSet1/tracks_final_dataset_clustered_sample.csv")

df = df[["danceability", "energy", "key", "loudness",  "mode", "speechiness","acousticness", "instrumentalness", "liveness", "valence", "tempo", "genres"]]

df["key"] = df["key"].apply(lambda x: key(x))
df["mode"] = df["mode"].apply(lambda x: mode(x))
df["genre"] = df["genres"].apply(lambda x: genre(x))
df = df.drop("genres", axis=1)

print(df.head())
df = df.dropna()
#df = df.iloc[:1000]
print(df.shape)
#df.to_csv('../resources/FinalDataset1/tracks_final_dataset_clustered1.csv')
famd = FAMD(n_components =5, n_iter = 3, random_state = 101)

famd.fit(df)
most_important = np.abs(famd.V_).argmax(axis=0)
initial_feature_names = df.columns
most_important_names = initial_feature_names[most_important]
dic = {'PC{}'.format(i+1): most_important_names[i] for i in range(5)}
pca_results = pd.DataFrame(dic.items())

print(pca_results)

#print(famd.explained_variance_)
famd.transform(df)

famd.plot_row_coordinates(df,figsize=(15, 10))
print("here")