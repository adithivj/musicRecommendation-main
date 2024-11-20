import pandas as pd
import json
import timeit


from sklearn.preprocessing import MinMaxScaler
from POC.utiltiy_function import *
start = timeit.timeit()
spotify_data = pd.read_csv('resources/track_data_spotify.csv', skipinitialspace = True)
spotify_data.head()



spotify_features_df = spotify_data

#spotify_features_df = spotify_features_df.drop(998)

# for j in spotify_features_df['loudness'][1:].values:
#     print( j)
#     print()

# print(spotify_features_df['loudness'].values)
# spotify_features_df['loudness'].str.strip();
spotify_features_df['acousticness'] = pd.to_numeric(spotify_features_df['acousticness'])

scaled_features = MinMaxScaler().fit_transform([
  spotify_features_df['acousticness'].values,
  spotify_features_df['danceability'].values,
  spotify_features_df['duration_ms'].values,
  spotify_features_df['energy'].values,
  spotify_features_df['instrumentalness'].values,
  spotify_features_df['liveness'].values,
  spotify_features_df['loudness'].values,
  spotify_features_df['speechiness'].values,
  spotify_features_df['tempo'].values,
  spotify_features_df['valence'].values,
  ])

spotify_features_df[['acousticness','danceability','duration_ms','energy','instrumentalness','liveness','loudness','speechiness','tempo','valence']] = scaled_features.T

with open('resources/mpd.slice.0-999.json') as json_file:
    data = json.load(json_file);

playlists = data['playlists'][0];

playlist_df = pd.DataFrame()


for i, play_track in enumerate(playlists['tracks']):
  playlist_df.loc[i, 'artist'] = play_track['artist_name']
  playlist_df.loc[i, 'track_name'] = play_track['track_name']
  print("track_uri ", play_track['track_uri'])
  playlist_df.loc[i, 'track_uri'] = play_track['track_uri']
  playlist_df.loc[i, 'date_added'] = "2017-12-03 08:41:42.057563"

#playlist_df['track_uri'] = playlist_df['track_uri'].str.replace('spotify:track:','')

playlist_df['date_added'] = pd.to_datetime(playlist_df['date_added'])

#print(playlist_df.head)

playlist_vector, nonplaylist_df = generate_playlist_vector(spotify_features_df, playlist_df, 1.2)
#print(playlist_vector.shape)
print("nonplaylist_df", nonplaylist_df.shape)


top15 = generate_recommendation(spotify_data, playlist_vector, nonplaylist_df)
top15.head()
end = timeit.timeit()
print(end - start)

#print(top15)



# spotify_features_nonplaylist = spotify_data.drop(['artist_genres', 'artist_name', 'artist_popularity'], axis=1)
# spotify_features_playlist = spotify_features_playlist.drop(['artist_genres', 'artist_name', 'artist_popularity'], axis=1)
#
# print(spotify_features_playlist.values)
# non_playlist = spotify_data[spotify_data['track_uri'].isin(spotify_features_nonplaylist['track_uri'].values)]
#
# spotify_features_nonplaylist =spotify_features_nonplaylist.drop(['track_uri'], axis=1)
# spotify_features_playlist = spotify_features_playlist.drop(['track_uri'], axis=1)
# print(spotify_features_nonplaylist.shape)
# print(spotify_features_playlist.shape)
# non_playlist['sim'] = cosine_similarity(spotify_features_nonplaylist.values,
#                                         spotify_features_playlist.values.reshape(1, -1))[:, 0]
# non_playlist_top15 = non_playlist.sort_values('sim', ascending=False).head(15)
#non_playlist_top15['url'] = non_playlist_top15['track_id'].apply(lambda x: sp.track(x)['album']['images'][1]['url'])
#print()


