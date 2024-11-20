import json;
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import csv
import pandas as pd

def addColumnData(row,artis_dic):

  if row in artis_dic.keys():
      values = artis_dic[row]
      return values
  else:
      return  []

  # if(len(values) > 1):
  #   return values[0]
  # else:
  #   return ""

def addColumnData1(row,artis_dic):
  if row in artis_dic.keys():
      values = artis_dic[row]
  else:
      return  ""

  if(len(values) > 2):
    return values[1]
  else:
    return ""

def addColumnData2(row,artis_dic):
    if row in artis_dic.keys():
        values = artis_dic[row]
    else:
        return ""

    if (len(values) > 3):
        return values[2]
    else:
        return ""

song_dataset_df = pd.read_csv('../resources/DatasetWithAssociatedArtists/tracks_final_associated_artists6.csv')

song_dataset_df['genres'] = song_dataset_df.apply(lambda _: '', axis=1)
#song_dataset_df['genre_2'] = song_dataset_df.apply(lambda _: '', axis=1)
#song_dataset_df['genre_3'] = song_dataset_df.apply(lambda _: '', axis=1)

print(song_dataset_df.columns)
print(len(pd.unique(song_dataset_df['artist1'])))

set_artist_id =set(song_dataset_df["artist1"])
list_artist_id = list(set_artist_id)

print(len(list_artist_id))

#print


artist_dict = {}
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id="af30624c87bc4f1a9b20a8463d2dd836", client_secret="5b613fc553cb4ab78c8a7044563fc899"))

i = 0
j=50
k=1
while(k<=341):
  artists = list_artist_id[i:j]
  i=i+50
  j= j+50
  artists = spotify.artists(artists);
  for artist in artists['artists']:
    artist_dict[artist["id"]] = artist["genres"]

  print(len(artist_dict))
  k=k+1




#for artist in artists['artists']:
# for artist in artists['artists']:
#   artist_dict[artist["id"]] = artist["genres"]

song_dataset_df['genres']=song_dataset_df.apply(lambda row: addColumnData(row['artist1'], artist_dict), axis=1)
#song_dataset_df['genre_1']=song_dataset_df.apply(lambda row: addColumnData(row['artist1'], artist_dict), axis=1)

#song_dataset_df['genre_2']=song_dataset_df.apply(lambda row: addColumnData1(row['artist1'], artist_dict), axis=1)

#song_dataset_df['genre_3']=song_dataset_df.apply(lambda row: addColumnData2(row['artist1'], artist_dict), axis=1)


song_dataset_df.to_csv('../resources/FinalDataset1/tracks_final_dataset6.csv')