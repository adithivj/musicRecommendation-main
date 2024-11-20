import pandas as pd
from sklearn import preprocessing
import seaborn as sns
import matplotlib.pyplot as plt



def dats_for_violin_plot():
    print("here")
    audio_features_df = pd.read_csv('./resources/tracks.csv')
    audio_features_df = pd.read_csv('./resources/tracks.csv')

    print(audio_features_df.head())

    audio_features_df1 = pd.read_csv("./resources/tracks.csv")
    audio_features_df1.drop(['duration_ms', 'popularity', 'id', 'name', 'explicit', 'artists', 'mode',
                             'id_artists', 'release_date', 'key'], axis=1, inplace=True)
    print(audio_features_df1.columns)

    x = audio_features_df1.values  # returns a numpy array
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled1 = min_max_scaler.fit_transform(x)
    df1 = pd.DataFrame(x_scaled1)
    df1.columns = ["danceability", "energy", "loudness", "speechiness", "acousticness", "instrumentalness", "liveness",
                   "valence", "tempo", 'time_signature']

    print(df1.columns)
    return df1








# for col in df1.columns:
#     print(col)
#
# ax = sns.heatmap(df1.cov(),vmin=-0.08, vmax=0.08, annot = True)
# plt.show()
#
# # distribution of features across all the songs in the track
# df2 = df1.melt(var_name='groups', value_name='vals')
# ax = sns.violinplot(x="groups", y="vals", data=df2, linewidth = 0.6, inner = 'point', scale= 'width')
# plt.show()
# print("here")