from userInterface.hello import *

playlist_tracks =pd.read_csv("../resources/output/playlist_tracks.csv")

# print(playlist_tracks.columns)
#
# tracks = playlist_tracks.track.unique()
# print(tracks)
#
# dataset = pd.read_csv("../resources/FinalDataSet1/tracks_final_dataset_clustered.csv")
#
# print("dataset shape ", dataset.shape)
#
# dataset_filtered_df = dataset[dataset['id'].isin(tracks)]
#
#
# print("dataset filtered shape ", dataset_filtered_df.shape)

#dataset_filtered_df.to_csv("../resources/FinalDataSet1/tracks_final_dataset_clustered_test.csv")


dataset_filtered_df =  loadNonNormalized("../resources/FinalDataSet1/tracks_final_dataset_clustered_test.csv")

def genre(x):
    row =x
    row = row.replace("[", "")
    row = row.replace("]", "")
    row = row.replace("'", "")
    row_list = row.split(", ")
    row = row_list[0]
    return row


dataset_filtered_df["genre"] = dataset_filtered_df["genres"].apply(lambda x: genre(x))

#get the tracks for each genre with highest playcount

#df_sorted = dataset_filtered_df.groupby(['genre'], as_index= False)['id','playcount'].apply(lambda x: x.nlargest(2, columns=['playcount']))

#get 15 hightest play count songs for the gnere Pop

# df_sorted_filtered = dataset_filtered_df[(dataset_filtered_df.genre == "pop")]
#
# df_sorted_filtered = df_sorted_filtered.sort_values(by =[ 'playcount'], ascending= False)
# df_sorted_filtered =df_sorted_filtered[0:15]


df_sorted_filtered = dataset_filtered_df.sort_values(by=['danceability'], ascending=False).head(15)


df_sorted_filtered.to_csv('../resources/FinalDataSet1/testResults/highest_danceability.csv')
songs = df_sorted_filtered.id.values



audio_features_df = loadData("../resources/FinalDataSet1/tracks_final_dataset_clustered_test.csv")
audio_features_non_normalized_df = loadNonNormalized("../resources/FinalDataSet1/tracks_final_dataset_clustered_test.csv")

audio_feature_df_dropped = drop_audio_features(audio_features_df)
song_features_df = audio_features_non_normalized_df[["id","name", "artists","duration_ms",  "release_date",'acousticness', 'danceability', 'duration_ms', 'energy', 'instrumentalness', 'liveness', 'loudness',
         'speechiness', 'tempo', 'valence','playcount','listeners' ]]

graph_songs = set()

recommended_df = getTop10Similar(songs, audio_features_df, audio_feature_df_dropped, song_features_df, graph_songs)

print(" recommended_df shape", recommended_df.shape)

recommended_df.to_csv("../resources/FinalDataSet1/testResults/top_genre_test_results_danceability.csv")

print("recommended_df ", recommended_df.columns)

print("playlist_tracks ", playlist_tracks.columns)

merged_df = pd.merge( playlist_tracks, recommended_df, right_on=["id"],   left_on=["track"], how="inner")

merged_df.to_csv("../resources/FinalDataSet1/testResults/top_genre_test_results_danceability.csv")



print("here")

# test data comprised of the songs of the same genre with highest play count

