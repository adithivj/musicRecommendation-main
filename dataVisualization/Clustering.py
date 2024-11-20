from sklearn.preprocessing import MinMaxScaler
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import normalize
from sklearn.preprocessing import StandardScaler

audio_features_df = pd.read_csv('../resources/FinalDataSet1/tracks_final_dataset_genres_encoded_sample.csv')

audio_features_df_listed_columns = audio_features_df[
    ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness',
     'speechiness', 'tempo', 'valence']]

audio_features_df_non_normalized =audio_features_df[
    ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness',
     'speechiness', 'tempo', 'valence']]

scaler = StandardScaler()
scaled_numeric_features = scaler.fit_transform([
    audio_features_df['acousticness'].values,
    audio_features_df['danceability'].values,
    audio_features_df['energy'].values,
    audio_features_df['instrumentalness'].values,
    audio_features_df['liveness'].values,
    audio_features_df['loudness'].values,
    audio_features_df['speechiness'].values,
    audio_features_df['tempo'].values,
    audio_features_df['valence'].values,
])

audio_features_df_listed_columns[
    ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness',
     'speechiness', 'tempo', 'valence']] = scaled_numeric_features.T


print(audio_features_df_listed_columns.columns)


# distortions = []
# K= range(1,10)
# for k in K:
#     kmeanModel = KMeans(n_clusters=k)
#     kmeanModel.fit(audio_features_df_listed_columns)
#     distortions.append(kmeanModel.inertia_)
#
# plt.figure(figsize=(16,8))
# plt.plot(K, distortions, 'bx-')
# plt.xlabel('k')
# plt.ylabel('Distortion')
# plt.title('The Elbow Method showing the optimal k')
# plt.show()


kmeanModel = KMeans(n_clusters=6)
kmeanModel.fit(audio_features_df_listed_columns)
audio_features_df_listed_columns["k_means"] = kmeanModel.predict(audio_features_df_listed_columns)

print(audio_features_df_listed_columns.columns)

print(audio_features_df_listed_columns['k_means'].head(200))

audio_features_df_non_normalized = pd.merge(audio_features_df, audio_features_df_listed_columns['k_means'], left_index=True, right_index=True)
#audio_features_df_listed_columns.to_csv('../resources/FinalDataset1/tracks_final_dataset_clustered.csv')

audio_features_df_non_normalized.to_csv('../resources/FinalDataset1/tracks_final_dataset_clustered_no_normalized_sample.csv')


# fig = plt.figure(figsize = (8,8))
#
# ax = fig.add_subplot(1,1,1)
#
# ax.set_xlabel('acousticness', fontsize = 15)
# ax.set_ylabel('danceability', fontsize = 15)
# ax.set_title('2 component cluster', fontsize = 20)
# targets = [0, 1,2,3,4]
# colors = ['r', 'g', 'b','y','pink']
# for target, color in zip(targets,colors):
#     indicesToKeep = audio_features_df_listed_columns['k_means'] == target
#     ax.scatter(audio_features_df_listed_columns.loc[indicesToKeep, 'acousticness']
#                , audio_features_df_listed_columns.loc[indicesToKeep, 'danceability']
#                , c = color
#                , s = 50)
# ax.legend(targets)
# ax.grid()
# print("here")


audio_features_df_listed_drop =audio_features_df_listed_columns.drop('k_means', axis=1)

#audio_features_df_listed = normalize(audio_features_df_listed_columns)


pca = PCA(n_components=2)

principalComponents = pca.fit_transform(audio_features_df_listed_drop)

print(pca.explained_variance_ratio_)

print(abs( pca.components_ ))


#plot_df = audio_features_df_listed[['acousticness','instrumentalness','k_means']]

fig = plt.figure(figsize = (20,20))

ax = fig.add_subplot(1,1,1)

ax.set_xlabel('acousticness', fontsize = 15)
ax.set_ylabel('danceability', fontsize = 15)
ax.set_title('Clsutered Plot', fontsize = 20)
targets = [0,1,2,3,4,5,6]

#targets = [3]
colors = ['darkred', 'darkorange', 'fuchsia','darkblue','yellow','green',"violet"]
for target, color in zip(targets,colors):
    indicesToKeep = audio_features_df_non_normalized['k_means'] == target
    ax.scatter(audio_features_df_non_normalized.loc[indicesToKeep, 'acousticness']
               , audio_features_df_non_normalized.loc[indicesToKeep, 'instrumentalness']
               , c = color
               , s = 50)
ax.legend(targets)
ax.grid()

principalDf = pd.DataFrame(data = principalComponents
             , columns = ['principal component 1', 'principal component 2'])

finalDf = pd.concat([principalDf, audio_features_df_listed_columns[['k_means']]], axis = 1)

finalDf.to_csv('../resources/FinalDataset1/tracks_final_dataset_clustered_pca.csv')

fig = plt.figure(figsize = (20,20))

ax = fig.add_subplot(1,1,1)

ax.set_xlabel('Principal Component 1', fontsize = 15)
ax.set_ylabel('Principal Component 2', fontsize = 15)
ax.set_title('2 component PCA', fontsize = 20)
targets = [0,1,2,3,4,5,6]

#targets = [3]
colors = ['darkred', 'darkorange', 'fuchsia','darkblue','yellow','green',"violet"]

#colors = ['darkblue']
for target, color in zip(targets,colors):
    indicesToKeep = finalDf['k_means'] == target
    ax.scatter(finalDf.loc[indicesToKeep, 'principal component 1']
               , finalDf.loc[indicesToKeep, 'principal component 2']
               , c = color
               , s = 50)
ax.legend(targets)
ax.grid()


# fig1 = plt.figure(figsize = (10,10))
#
# ax1 = fig1.add_subplot(1,1,1)
#
# ax1.set_xlabel('Principal Component 1', fontsize = 15)
# ax1.set_ylabel('Principal Component 2', fontsize = 15)
# ax1.set_title('2 component PCA', fontsize = 20)
# targets = [0]
# colors = ['darkred']
# for target, color in zip(targets,colors):
#     indicesToKeep = finalDf['k_means'] == target
#     ax1.scatter(finalDf.loc[indicesToKeep, 'principal component 1']
#                , finalDf.loc[indicesToKeep, 'principal component 2']
#                , c = color
#                , s = 50)
# ax1.legend(targets)
# ax1.grid()
#
#
#
# fig2 = plt.figure(figsize = (10,10))
#
# ax2 = fig2.add_subplot(1,1,1)
#
# ax2.set_xlabel('Principal Component 1', fontsize = 15)
# ax2.set_ylabel('Principal Component 2', fontsize = 15)
# ax2.set_title('2 component PCA', fontsize = 20)
# targets = [1]
# colors = ['darkorange']
# for target, color in zip(targets,colors):
#     indicesToKeep = finalDf['k_means'] == target
#     ax2.scatter(finalDf.loc[indicesToKeep, 'principal component 1']
#                , finalDf.loc[indicesToKeep, 'principal component 2']
#                , c = color
#                , s = 50)
# ax2.legend(targets)
# ax2.grid()
#
#
# fig3 = plt.figure(figsize = (10,10))
#
# ax3 = fig3.add_subplot(1,1,1)
#
# ax3.set_xlabel('Principal Component 1', fontsize = 15)
# ax3.set_ylabel('Principal Component 2', fontsize = 15)
# ax3.set_title('2 component PCA', fontsize = 20)
# targets = [2]
# colors = ['fuchsia']
# for target, color in zip(targets,colors):
#     indicesToKeep = finalDf['k_means'] == target
#     ax3.scatter(finalDf.loc[indicesToKeep, 'principal component 1']
#                , finalDf.loc[indicesToKeep, 'principal component 2']
#                , c = color
#                , s = 50)
# ax3.legend(targets)
# ax3.grid()
#
# fig4 = plt.figure(figsize = (10,10))
#
# ax4 = fig4.add_subplot(1,1,1)
#
# ax4.set_xlabel('Principal Component 1', fontsize = 15)
# ax4.set_ylabel('Principal Component 2', fontsize = 15)
# ax4.set_title('2 component PCA', fontsize = 20)
# targets = [3]
# colors = ['darkblue']
# for target, color in zip(targets,colors):
#     indicesToKeep = finalDf['k_means'] == target
#     ax4.scatter(finalDf.loc[indicesToKeep, 'principal component 1']
#                , finalDf.loc[indicesToKeep, 'principal component 2']
#                , c = color
#                , s = 50)
# ax4.legend(targets)
# ax4.grid()
#
print("here")