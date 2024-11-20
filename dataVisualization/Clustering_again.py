import numpy as np

import matplotlib.pyplot as plt

import pandas as pd

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA


dataset = pd.read_csv("/Users/pk/Learn/CSE-6242/workspace/CSE6242-project-team-16/resources/FinalDataSet1/tracks_final_dataset_genres_encoded_new.csv")
print(dataset.columns)
# dff= dataset[['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness',
#      'speechiness', 'tempo', 'valence','key','mode','playcount','listeners']]
dataset = dataset.drop(['Unnamed: 0','Unnamed: 0.1'] , axis=1)
dff = dataset.drop(['name','time_signature','artist1','associatedArtist1','associatedArtist2','associatedArtist3','genres' ], axis=1)

# feature = dataset.columns[2:23]
# # print(features)
# fea = [ 'time_signature', 'explicit', 'associatedArtist1', 'associatedArtist2', 'associatedArtist3',
#        'artists', 'artist1', 'release_date']
# features = [f for f in feature if f not in fea]


# features


# In[3]:


# [reference:https://careerfoundry.com/en/blog/data-analytics/how-to-find-outliers/]
def find_outliers_IQR(df):
    q1 = df.quantile(0.25)

    q3 = df.quantile(0.75)

    IQR = q3 - q1

    outliers = df[((df < (q1 - 1.5 * IQR)) | (df > (q3 + 1.5 * IQR)))]

    return outliers


outliers = find_outliers_IQR(dff['duration_ms'])

# In[4]:


dff_copy = dataset.copy()
#dfff = dff_copy.drop(outliers.index, axis=0).reset_index(drop=True)
print(dff.columns)


# In[5]:


import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

values = dff[['energy', 'danceability']]


wcss_song = []
cluster_song = []
for i in range(1, 21):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
    kmeans.fit(values)
    cluster_song.append(i)
    wcss_song.append(kmeans.inertia_)

# In[18]:


plt.plot(cluster_song, wcss_song)
plt.xticks(np.arange(0, 21, step=2))
plt.axvline(5, linestyle='--', color='r')
plt.title("Elbow Plot")
plt.xlabel("NO. of Clusters")
plt.ylabel("WCSS")

# In[7]:


kmeans_song = KMeans(n_clusters=5, random_state=42)
kmeans_song.fit(values)
values['id'] = dataset['id']
values['name'] = dataset['name']
values['clusters'] = kmeans_song.labels_
# sns.scatterplot(x = values['energy'], y = values['danceability'], hue=values['clusters'])


dataset = pd.merge(dataset, values['clusters'], left_index=True, right_index=True)
dataset = dataset.dropna()
dataset.to_csv('../resources/FinalDataset1/tracks_final_dataset_clustered.csv')
# pca = PCA(n_components=2)
#
# principalComponents = pca.fit_transform(dff)
#
# print(pca.explained_variance_ratio_)
#
# print(abs( pca.components_ ))
#
# principalDf = pd.DataFrame(data = principalComponents
#              , columns = ['principal component 1', 'principal component 2'])
#
# finalDf = pd.concat([principalDf, values['clusters']], axis = 1)
#
# fig = px.scatter(values, x=values['energy'], y=values['danceability'], color=values['clusters'],
#                  hover_data=[values['energy'], values['danceability'], values['name']])
# fig.show()

import plotly.express as px

fig = px.scatter(values, x=values['energy'], y=values['danceability'], color=values['clusters'],
                 hover_data=[values['energy'], values['danceability'], values['name']])
fig.show()

print('here')
