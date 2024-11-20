#!/usr/bin/env python
# coding: utf-8

# In[1]:


# %load clustering_2features.py
#!/usr/bin/env python

import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')
df=pd.read_csv("tracks_final_dataset_genres_encoded.csv")
df.head(5)
feature=df.columns[2:23]
#print(features)
fea=['key', 'mode', 'time_signature', 'explicit', 'associatedArtist1', 'associatedArtist2', 'associatedArtist3', 'artists', 'artist1', 'release_date']
features=[f for f in feature if f not in fea]
#features

df1=df[features]


# In[2]:


#[reference:https://careerfoundry.com/en/blog/data-analytics/how-to-find-outliers/]
def find_outliers_IQR(df):

    q1=df.quantile(0.25)

    q3=df.quantile(0.75)

    IQR=q3-q1

    outliers = df[((df<(q1-1.5*IQR)) | (df>(q3+1.5*IQR)))]
  
    return outliers

outliers = find_outliers_IQR(df1['duration_ms'])


# In[3]:


dff_copy=df1.copy()
dfff=dff_copy.drop(outliers.index, axis=0).reset_index(drop=True)


# In[4]:


import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
values = dfff[['energy', 'danceability']]
values1 = dfff[['valence', 'acousticness']]
values2=dfff[['liveness', 'instrumentalness']]
values3=dfff[['tempo', 'instrumentalness']]
values4=dfff[['valence', 'tempo']]
values5=dfff[['speechiness', 'loudness']]
#values5=dfff[['speechiness', 'energy']]


# In[5]:


def elbow_plot(df):
    wcss_song = []
    cluster_song=[]
    for i in range(1, 21): 
        kmeans = KMeans(n_clusters = i, init = 'k-means++', random_state = 42)
        kmeans.fit(values) 
        cluster_song.append(i)
        wcss_song.append(kmeans.inertia_)

    plt.plot(cluster_song, wcss_song)
    plt.xticks(np.arange(0, 21, step=2))
    #plt.axvline(5, linestyle='--', color='r')
    plt.title("Elbow Plot")
    plt.xlabel("NO. of Clusters")
    plt.ylabel("WCSS")
    plt.show()
    return


# In[6]:


def clustering_plot(c, df, f1, f2):
    kmeans_song = KMeans(n_clusters=c, random_state=42)
    kmeans_song.fit(df)
    ddf=df.copy()
    #ddf['id']=dfff['id']
    ddf['name']=dfff['name']
    ddf['clusters']=kmeans_song.labels_
    #fig = px.scatter(ddf, x= f1, y=f2, color='clusters', hover_data=[ddf[f1], ddf[f2], ddf['name']])
    fig = px.scatter(ddf, x= f1, y=f2, color='clusters')
    fig.show()
    return ddf


# In[ ]:


#elbow_plot(values)


# In[7]:


values_1=clustering_plot(5, values, 'energy', 'danceability')


# In[ ]:


#elbow_plot(values1)


# In[8]:


values_2=clustering_plot(4, values1, 'valence', 'acousticness')


# In[ ]:


#elbow_plot(values2)


# In[9]:


values_3=clustering_plot(3, values2, 'instrumentalness', 'liveness')


# In[10]:


from sklearn.preprocessing import StandardScaler
def df_scaled(df):
    featu=df.columns
    x_df=df.copy()
    #x_df = df[features]
    x_array=x_df.values
    X_array=StandardScaler().fit_transform(x_array)
    X = pd.DataFrame(X_array, columns = featu)
    return X


# In[11]:


values3_scaled=df_scaled(values3)


# In[ ]:


#elbow_plot(values3_scaled)


# In[12]:


values_4=clustering_plot(4, values3_scaled, 'instrumentalness', 'tempo')


# In[13]:


values4_scaled=df_scaled(values4)
#elbow_plot(values4_scaled)
#values_5=clustering_plot()


# In[ ]:


#elbow_plot(values4_scaled)


# In[14]:


values_5=clustering_plot(4, values4_scaled, 'valence', 'tempo')


# In[15]:


values5_scaled=df_scaled(values5)
#elbow_plot(values5)


# In[ ]:


#elbow_plot(values5_scaled)


# In[16]:


values_6=clustering_plot(4, values5_scaled, 'loudness', 'speechiness')

