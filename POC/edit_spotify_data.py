import pandas as pd

spotify_data = pd.read_csv('resources/SpotifyFeatures.csv', skipinitialspace = True)
spotify_data.head()

spotify_data = spotify_data.drop(['genre','artist_name','track_name','key','mode','time_signature'], axis=1)

print(spotify_data.columns)

spotify_data =spotify_data[['danceability', 'energy', 'loudness', 'speechiness', 'acousticness'
                            , 'instrumentalness', 'liveness', 'liveness', 'valence', 'tempo'
                            ,'duration_ms', 'popularity', 'track_uri']]
spotify_data['track_uri'] =  spotify_data['track_uri'].map('spotify:track:{}'.format)

spotify_data.to_csv('resources/track_data_spotify.csv', sep=',', mode='a', index=False, header=True)

#spotify_data.to_csv('resources/track_data_spotify', sep=',')