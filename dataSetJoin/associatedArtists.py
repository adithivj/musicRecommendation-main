import json;
import pandas as pd;


def extract_artist2(row):
    x = row.split(',')
    if (len(x) >=2):
        return x[1]
    else:
        return ""

def extract_artist3(row):
    x = row.split(',')
    if (len(x) >=3):
        return x[2]
    else:
        return ""
def extract_artist1(row):
    x = row.split(',')
    artist_uri = x[0].replace("'", "")

    return artist_uri

df_track = pd.read_csv('../resources/tracks-1.csv')

df_playlist_track_artists = pd.read_csv('../resources/playlist_tracks_artists.csv')

df_track["id_artists"] = df_track["id_artists"].str.replace("[", "")

df_track["id_artists"] = df_track["id_artists"].str.replace("]", "")

df_track['artist1'] = df_track['id_artists'].str.split(',', expand=True)[0]

df_track['artist1'] = df_track.apply(lambda row: extract_artist1(row['id_artists']), axis=1)

#df_track['artist2'] = df_track.apply(lambda row: extract_artist2(row['id_artists']), axis=1)

#df_track['artist3'] = df_track.apply(lambda row: extract_artist3(row['id_artists']), axis=1)


df_track = df_track.drop("id_artists",axis=1)

df_track.to_csv('../resources/tracks_final.csv')
print(df_track.columns)
