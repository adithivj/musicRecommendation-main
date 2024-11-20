from sklearn.metrics.pairwise import cosine_similarity

def generate_playlist_vector(spotify_features_df, playlist_df, weight_factor):

  spotify_features_playlist = spotify_features_df[spotify_features_df['track_uri'].isin(playlist_df['track_uri'].values)]
  spotify_features_playlist = spotify_features_playlist.merge(playlist_df[['track_uri', 'date_added']], on='track_uri',
                                                            how='inner')

  spotify_features_nonplaylist = spotify_features_df[~spotify_features_df['track_uri'].isin(playlist_df['track_uri'].values)]

  #spotify_features_playlist = spotify_features_playlist.drop(['artist_genres', 'artist_name', 'artist_popularity'],
                                                      #      axis=1)

  playlist_feature_set = spotify_features_playlist.sort_values('date_added', ascending=False)


  most_recent_date = playlist_feature_set.iloc[0, -1]

  for ix, row in playlist_feature_set.iterrows():
    playlist_feature_set.loc[ix, 'days_from_recent'] = int(
      (most_recent_date.to_pydatetime() - row.iloc[-1].to_pydatetime()).days)

  playlist_feature_set['weight'] = playlist_feature_set['days_from_recent'].apply(lambda x: weight_factor ** (-x))
  playlist_feature_set_weighted = playlist_feature_set.copy()

  playlist_feature_set_weighted.update(
    playlist_feature_set_weighted.iloc[:, :-3].mul(playlist_feature_set_weighted.weight.astype(int), 0))

  playlist_feature_set_weighted_final = playlist_feature_set_weighted.iloc[:, :-3]

  return playlist_feature_set_weighted_final.sum(axis = 0), spotify_features_nonplaylist


def generate_recommendation(spotify_data, playlist_vector, nonplaylist_df):
    non_playlist = spotify_data[spotify_data['track_uri'].isin(nonplaylist_df['track_uri'].values)]
    #non_playlist = non_playlist.drop(['artist_genres', 'artist_name', 'artist_popularity'], axis=1)
    #nonplaylist_df = nonplaylist_df.iloc[:950, ];

    print("playlist_vector ",playlist_vector.to_string())
    print(playlist_vector.shape)
    print(playlist_vector.shape)
    non_playlist['sim'] = cosine_similarity(non_playlist.drop(['track_uri'], axis=1).values,
                                            playlist_vector.drop(labels='track_uri').values.reshape(1, -1))[:, 0]

    print("non_playlist ", non_playlist.shape)
    non_playlist_top15 = non_playlist.sort_values('sim', ascending=False).head(15)

    return non_playlist_top15