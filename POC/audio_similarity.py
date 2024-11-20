import json;
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import csv

class Track:
  def __init__(self, track_uri, artist_uri, album_uri):
    self.track_uri = track_uri
    self.artist_uri = artist_uri
    self.album_uri = album_uri


with open('resources/mpd.slice.0-999.json') as json_file:
    data = json.load(json_file);

playlists = data['playlists'];

#Iterate through list of dicts and generate a set with track uris

track_uris = set()

for playlist in playlists:
    tracks = playlist['tracks'];
    for track in tracks:
        track = Track(track['track_uri'], track['artist_uri'], track['album_uri'])
        track_uris.add(track);

final_data_list = []

#spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id="9af4046aa77c48a392157c9d5eb6ccd7", client_secret="bbef58ed0c9b4fc9b1b7dc0e36da4362"))

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id="af30624c87bc4f1a9b20a8463d2dd836", client_secret="5b613fc553cb4ab78c8a7044563fc899"))


trackuris_sliced = list(track_uris)[15001:17000]

for track in trackuris_sliced:
    tracks = [];
    tracks.append(track.track_uri)
    audio_features_track = spotify.audio_features(tracks = tracks);
    audio_track_infos = spotify.tracks(tracks = tracks);
    audio_track_info = audio_track_infos['tracks'];

    #album = spotify.album(album_id = track.album_uri)

    artist = spotify.artist(track.artist_uri);

    print("here audio_features ", audio_features_track[0]);

    print(" here track info ", audio_track_info[0]);

    print("here artist ", artist)

    keys_from_audio_features_track = ['acousticness','danceability', 'energy','loudness', 'speechiness','instrumentalness',
                                      'liveness','valence','tempo', 'duration_ms'];
    keys_from_audio_track_infos = ['popularity', 'uri'];
    keys_from_artist = ['name', 'popularity', 'genres']

    #keys_from_album = ['genres']

    z = {}
    for key,value in audio_features_track[0].items():
        if(key in keys_from_audio_features_track):

            z.update({key:value});

    for key, value in audio_track_info[0].items():
        if (key in keys_from_audio_track_infos):
            if (key == 'uri'):
                key = 'track_uri'
            z.update({key: value});

    for key, value in artist.items():
        if (key in keys_from_artist):
            if (key == 'genres'):
                value_string = ("|").join(value)
                z.update({"artist_" + key: value_string});
            else:
                z.update({"artist_" + key: value});




    final_data_list.append(z);

keys = final_data_list[0].keys()

with open('resources/track_data.csv', 'a') as output_file:
        dict_writer = csv.DictWriter(output_file,keys)
        #dict_writer.writeheader()
        dict_writer.writerows(final_data_list)


#spotify.albums()
print ("here ", len(track_uris));

