import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

#Load data during start of the application

def loadData(filepath):
    audio_features_df = pd.read_csv(filepath)
    audio_features_df = normalizeNumericData(audio_features_df)

    return audio_features_df

def loadNonNormalized(filepath):
    audio_features_df = pd.read_csv(filepath)
    return audio_features_df


def drop_audio_features(audio_features_df):
    audio_features_df = audio_features_df.drop(
        [ "name", "popularity", "duration_ms", "explicit", "artists",
         "release_date", "time_signature", "artist1",
         "associatedArtist1", "associatedArtist2", "associatedArtist3","genres","clusters"], axis=1)
    return audio_features_df

def normalizeNumericData(audio_features_df):
    scaled_numeric_features = MinMaxScaler().fit_transform([
        audio_features_df['acousticness'].values,
        audio_features_df['danceability'].values,
        audio_features_df['duration_ms'].values,
        audio_features_df['energy'].values,
        audio_features_df['instrumentalness'].values,
        audio_features_df['liveness'].values,
        audio_features_df['loudness'].values,
        audio_features_df['speechiness'].values,
        audio_features_df['tempo'].values,
        audio_features_df['valence'].values,
        audio_features_df['playcount'].values,
        audio_features_df['listeners'].values,
    ])

    audio_features_df[
        ['acousticness', 'danceability', 'duration_ms', 'energy', 'instrumentalness', 'liveness', 'loudness',
         'speechiness', 'tempo', 'valence','playcount','listeners']] = scaled_numeric_features.T
    return audio_features_df

def generate_recommendation(song_vector, track_dataset):


    print("song_vector ",song_vector.to_string())
    print(track_dataset.shape)

    track_dataset['sim'] = cosine_similarity(track_dataset.drop(['id'], axis=1).values,
                                             song_vector.drop(labels='id').values.reshape(1, -1))[:, 0]

    print("song_vector ", song_vector.shape)
    track_dataset_top15 =track_dataset.sort_values('sim', ascending=False).head(15)

    return track_dataset_top15


def getTop10Similar(song_dictionary, audio_features_df, audio_feature_df_dropped, song_features_df, graph_songs):
    # audio_features_df = loadData('../resources/FinalDataSet1/tracks_final_dataset_genres_encoded.csv')
    # audio_feature_df_dropped = drop_audio_features(audio_features_df)
    # song_features_df = audio_features_df[["id","name", "artists","duration_ms",  "release_date"]]

    song_df  = pd.DataFrame(song_dictionary, columns=[ 'id'])
    input_song_features_df = audio_feature_df_dropped[
        audio_feature_df_dropped['id'].isin(song_df['id'].values)]

    print(audio_features_df.shape)
    audio_features_without_song_df = audio_feature_df_dropped[
        ~audio_feature_df_dropped['id'].isin(input_song_features_df['id'].values)]

    audio_features_without_song_df = audio_feature_df_dropped[
        ~audio_feature_df_dropped['id'].isin(graph_songs)]

    print("input_song_features_df", input_song_features_df.shape)
    print(audio_features_without_song_df.shape)
    input_song_features_vector = input_song_features_df.sum(axis=0)
    recommendations = generate_recommendation(input_song_features_vector, audio_features_without_song_df)
    id_list= recommendations['id'].tolist()
    recommendation_songs = song_features_df[song_features_df['id'].isin(id_list)]
    return recommendation_songs, recommendations



# songs = ["4qlfHfF422rd3I1FOs6N4s"]
# recommendations = getTop10Similar(songs)
#
# print(recommendations.head())x

#print(recommendations["acousticness"])
