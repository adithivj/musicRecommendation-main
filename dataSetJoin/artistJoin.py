import json;
import pandas as pd;

#The code below will read the playlist file and append to the playlist_artist.csv

with open('../resources/mpd.slice.164000-164999.json') as json_file:
    data = json.load(json_file);

playlists = data['playlists'];

df = pd.DataFrame(columns=['playlist_name', 'track_uri', 'artist_uri'])

for playlist in playlists:
    print(playlist)
    for track in playlist['tracks']:
        df = df.append({'playlist_name':playlist['name'], 'track_uri':track['track_uri'], 'artist_uri':track['artist_uri']}, ignore_index=True)



df.to_csv('../resources/playlist_tracks_artists.csv',mode='a', index=False, header=False)