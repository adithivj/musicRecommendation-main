import json;
import pandas as pd;


df_playlist0 =  pd.read_csv('../resources/playlist_tracks_artists0.csv', header= None, names=["playlist_name", "track_uri", "artist_uri"])

df_playlist1 =  pd.read_csv('../resources/playlist_tracks_artists1.csv', header= None, names=["playlist_name", "track_uri", "artist_uri"])

df_playlist2 =  pd.read_csv('../resources/playlist_tracks_artists2.csv', header= None, names=["playlist_name", "track_uri", "artist_uri"])

df_playlist3 =  pd.read_csv('../resources/playlist_tracks_artists3.csv', header= None, names=["playlist_name", "track_uri", "artist_uri"])

df_playlist4 =  pd.read_csv('../resources/playlist_tracks_artists4.csv', header= None, names=["playlist_name", "track_uri", "artist_uri"])

df_playlist5 =  pd.read_csv('../resources/playlist_tracks_artists5.csv', header= None, names=["playlist_name", "track_uri", "artist_uri"])

df_playlist6 =  pd.read_csv('../resources/playlist_tracks_artists6.csv', header= None, names=["playlist_name", "track_uri", "artist_uri"])

df_playlist = pd.DataFrame(columns=['playlist_name', 'track_uri', 'artist_uri'])

df_playlist = df_playlist.append(df_playlist0)

df_playlist = df_playlist.append(df_playlist1)

df_playlist = df_playlist.append(df_playlist2)

df_playlist = df_playlist.append(df_playlist3)

df_playlist = df_playlist.append(df_playlist4)

df_playlist = df_playlist.append(df_playlist5)

df_playlist = df_playlist.append(df_playlist6)

#print(df_playlist.head(10))

#print(df_playlist.count())

#print(df_playlist2.count())

#artis_count
#df_playlist_count_artist = df_playldf_playlist_gp1ist.groupby("artist_uri").count()

#print(df_playlist_count_artist.head(10))

#df_playlist_count_artist.to_csv('../resources/artists_count.csv')

#df_playlist0_filter = df_playlist0.query('artist_uri == "03a5eVjzFyQlR4XyVSwt4t"')

df_playlist_gp1 =  df_playlist.groupby("playlist_name")['artist_uri'].unique()

#print(df_playlist0_gp1.columns)

#df_playlist0_gp1["artist_list_count"] = len(df_playlist0_gp1['playlist_name'])
#df_playlist_gp1.to_csv('../resources/artists_count.csv')

df_playlist_gp = pd.DataFrame.from_records(df_playlist_gp1.values.tolist()).stack().value_counts()
#
#df_playlist_gp.to_csv('../resources/artists_gp.csv')
df_playlist_artist_count =  pd.DataFrame({'artist':df_playlist_gp.index, 'count_in_playlists':df_playlist_gp.values})
#df_playlist playlists_tracks_artists



# Please provide the input file here

df_tracks = pd.read_csv('../resources/track_final1.csv')

#print(df_playlist_artist_count.head(10))

df_tracks['associatedArtist1'] = df_tracks.apply(lambda _: '', axis=1)
df_tracks['associatedArtist2'] = df_tracks.apply(lambda _: '', axis=1)
df_tracks['associatedArtist3'] = df_tracks.apply(lambda _: '', axis=1)

print(df_tracks['id'].iloc[0])

print(df_tracks.columns)
j=-1;


for index, row in df_tracks.iterrows():
    j= j+1
    print("j ", j)
    print("index ", index)
    id = row["id"]
    artist = row["artist1"]
    df_playlist_filter_track = df_playlist.query('track_uri == @id')
    df_playlist_filter_artist = df_playlist.query('artist_uri == @artist')
    i=0
    if not df_playlist_filter_artist.empty:
       playlist_list  = df_playlist_filter_artist['playlist_name'].tolist()
       df_playlist_all_playlists_rows  = df_playlist[df_playlist['playlist_name'].isin(playlist_list)]
       artists = df_playlist_all_playlists_rows['artist_uri'].tolist()

       df_playlist_artist_count_filter = df_playlist_artist_count[df_playlist_artist_count['artist'].isin(artists)].sort_values(by=['count_in_playlists'], ascending=False)


       for ind, artist1 in df_playlist_artist_count_filter.iterrows():
           if(i == 0 ):
               df_tracks.at[index, 'associatedArtist1'] = artist1['artist']

           elif(i == 1 ):
               df_tracks.at[index, 'associatedArtist2'] = artist1['artist']
           elif(i == 2 ):
               df_tracks.at[index, 'associatedArtist3'] = artist1['artist']
               break
           i= i+1
           print("inside here")
       #print(df_playlist_all_playlists_rows)as
       #print(df_playlist_artist_count_filter['count_in_playlists'].nlargest(3))
       #print(df_playlist_artist_count_filter.head(10))
    elif not df_playlist_filter_track.empty:
        playlist_list = df_playlist_filter_track['playlist_name'].tolist()
        df_playlist_all_playlists_rows = df_playlist[df_playlist['playlist_name'].isin(playlist_list)]

        artists = df_playlist_all_playlists_rows['artist_uri'].tolist()
        df_playlist_track_count_filter = df_playlist_artist_count[
            df_playlist_artist_count['artist'].isin(artists)].sort_values(by=['count_in_playlists'], ascending=False)
        for ind, artist2 in df_playlist_artist_count_filter.iterrows():
            if (i == 0):
                df_tracks.at[index, 'associatedArtist1'] = artist1['artist']
            elif (i == 1):
                df_tracks.at[index, 'associatedArtist2'] = artist1['artist']
            elif (i == 2):
                df_tracks.at[index, 'associatedArtist3'] = artist1['artist']
            i=i+1


# This is the output file . Please update per run of the input file
df_tracks.to_csv('../resources/tracks_final_associated_artists1.csv')
#df_playlist_join = pd.merge(df_tracks, df_playlist, left_on='id',right_on='track_uri',how='inner',suffixes=('_left','_right'))



#