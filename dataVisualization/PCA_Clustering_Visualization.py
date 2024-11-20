#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

df=pd.read_csv("tracks_final_dataset_genres_encoded.csv")
df.head(5)
#column_list=df.columns.tolist()
#print(column_list)
#feature=df.select_dtypes(np.number).columns.tolist()[2:23]
#print(features)
#fea=['key', 'mode', 'time_signature', 'explicit', 'valence','liveness', 'loudness', 'popularity', 'associatedArtist1', 'associatedArtist2', 'associatedArtist3', 'artists', 'artist1', 'release_date'] 
#'popularity', 'explicit', 'liveness', 'loudness']
#features=[f for f in feature if f not in fea]
#df[features]
#features
feature=df.columns[2:23]
#print(features)
fea=['key', 'mode', 'time_signature', 'explicit', 'popularity','associatedArtist1', 'associatedArtist2', 'associatedArtist3', 'artists', 'artist1', 'release_date']
#, 'valence','liveness', 'loudness'
features=[f for f in feature if f not in fea]
features
#ax = sns.heatmap(df[features].corr(), annot=True)


# In[2]:


df[feature].describe()


# In[3]:


fig = px.histogram(df[features], x='duration_ms')
#fig = px.histogram(df[feature], x='mode')
fig.show()


# In[4]:


fig = px.box(df[features], x='duration_ms')

fig.show()


# In[5]:


#[reference:https://careerfoundry.com/en/blog/data-analytics/how-to-find-outliers/]
dff=df[features]
#create a function to find outliers using IQR

def find_outliers_IQR(df):

    q1=df.quantile(0.25)

    q3=df.quantile(0.75)

    IQR=q3-q1

    outliers = df[((df<(q1-1.5*IQR)) | (df>(q3+1.5*IQR)))]
  

    return outliers

outliers = find_outliers_IQR(dff['duration_ms'])


print('number of outliers: '+ str(len(outliers)))

print('max outlier value: '+ str(outliers.max()))

print('min outlier value: '+ str(outliers.min()))


# In[6]:


#drop outliers
dff_copy=dff.copy()
dfff=dff_copy.drop(outliers.index, axis=0).reset_index(drop=True)
dfff=dfff.drop('duration_ms', axis=1)
dfff.head()


# In[7]:




# Scale the features before applying PCA 
# [https://www.geeksforgeeks.org/implementing-pca-in-python-with-scikit-learn/]
featu=dfff.columns[2:]
x_df=dfff[featu]
#x_df = df[features]
x_array=x_df.values
X_array=StandardScaler().fit_transform(x_array)
X = pd.DataFrame(X_array, columns = featu)

# Apply PCA
pca_out = PCA().fit(X)

# Proportion of Variance (from PC1 to PC15)
# get eigenvalues (variance explained by each PC)
variance = pca_out.explained_variance_
prop_var=pca_out.explained_variance_ratio_
print("variance explained by each PC", variance)
print("Proportion of Variance", prop_var)

# Cumulative proportion of variance (from PC1 to PC6)   
c_prop_var=np.cumsum(prop_var)
print("Cumulative proportion of variance", c_prop_var)


# component loadings or weights (correlation coefficient between original variables and the component) 
# component loadings represents the elements of the eigenvector
# the squared loadings within the PCs always sums to 1
#[https://www.reneshbedre.com/blog/principal-component-analysis.html]
loadings = pca_out.components_
num_pc = pca_out.n_features_
pc_list = ["PC"+str(i) for i in list(range(1, num_pc+1))]
loadings_df = pd.DataFrame.from_dict(dict(zip(pc_list, loadings)))
loadings_df['variable'] = X.columns.values
loadings_df = loadings_df.set_index('variable')
loadings_df = loadings_df.round(2)


# get correlation matrix plot for loadings
# positive and negative values in component loadings reflects the positive and negative 
# correlation of the variables with the PCs.
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(rc = {'figure.figsize':(15,15)})
ax = sns.heatmap(loadings_df, annot=True, cmap='Spectral')
plt.show()


# In[8]:


#ax = sns.heatmap(df[feature].corr(), annot=True)


# In[9]:


#Scree Plot
sns.set(rc = {'figure.figsize':(15,8)})
fig, ax1 =plt.subplots()
ax1.bar(pc_list, prop_var*100)
ax1.set_xlabel('PCs', fontsize=16)
ax1.set_ylabel('Proportion of Variance (%)', fontsize=16)
ax1.set_ylim(0,35)
ax1.legend(['proportion of variance (%)'], loc="upper left", fontsize=13)

ax2=ax1.twinx()
ax2.plot(np.cumsum(pca_out.explained_variance_ratio_), color="red")
ax2.grid(False)
ax2.set_ylabel('cumulative explained variance', fontsize=16)
ax2.legend(['cumulative explained variance'], loc="upper center", fontsize=13)
plt.show()


# In[10]:


#[https://github.com/reneshbedre/bioinfokit]
#[Renesh Bedre. (2020, March 5). reneshbedre/bioinfokit: Bioinformatics data analysis and visualization toolkit. Zenodo.
#http://doi.org/10.5281/zenodo.3698145.]

from bioinfokit.visuz import cluster
# get PC scores
pca_scores = PCA().fit_transform(X)

# get 2D biplot
cluster.biplot(cscore=pca_scores, loadings=loadings, labels=X.columns.values, var1=round(pca_out.explained_variance_ratio_[0]*100, 2),
    var2=round(pca_out.explained_variance_ratio_[1]*100, 2), axlabelfontsize=12, show=True, dim=(10, 10))


# get 3D biplot
cluster.biplot(cscore=pca_scores, loadings=loadings, labels=X.columns.values, 
    var1=round(pca_out.explained_variance_ratio_[0]*100, 2), var2=round(pca_out.explained_variance_ratio_[1]*100, 2), 
    var3=round(pca_out.explained_variance_ratio_[2]*100, 2), show=True, valphadot=0.5, dim=(15, 15))


# In[11]:


##[reference:https://towardsdatascience.com/how-to-build-an-amazing-music-recommendation-system-4cce2719a572]
from sklearn.cluster import KMeans
pca_pipeline = Pipeline([('scaler', StandardScaler()), ('PCA', PCA(n_components=2))])
song_embedding = pca_pipeline.fit_transform(x_df)
projection = pd.DataFrame(columns=['PC1', 'PC2'], data=song_embedding)
kmeans_song = KMeans(n_clusters=4, random_state=42)
kmeans_song.fit(projection)
projection['clusters']=kmeans_song.labels_


# In[12]:


##[reference:https://stackabuse.com/k-means-clustering-with-scikit-learn/]
wcss_song = []
cluster_song=[]

for i in range(1, 21): 
    kmeans = KMeans(n_clusters = i, init = 'k-means++', random_state = 42)
    kmeans.fit(projection) 
    cluster_song.append(i)
    new_inertia=kmeans.inertia_
    wcss_song.append(new_inertia)
    
plt.plot(cluster_song, wcss_song)
plt.xticks(np.arange(0, 21, step=2))
plt.title("Elbow Plot")
plt.xlabel("NO. of Clusters")
plt.ylabel("WCSS")
#plt.axvline(4, linestyle='--', color='r')
plt.show()


# In[13]:


projection['name'] = dfff['name']
projection['id'] = dfff['id']


# In[14]:


#Clustering Plot
import plotly.express as px
fig = px.scatter(projection, x='PC1', y='PC2', color='clusters', hover_data=['PC1', 'PC2'])
fig.show()


# In[15]:


#Clustering_loading plot
##[reference:https://plotly.com/python/pca-visualization/]
loadings1 = pca_out.components_.T*np.sqrt(pca_out.explained_variance_)*4
#* np.sqrt(pca.explained_variance_)
f=dfff.columns[2:]
#fig = px.scatter(components, x=0, y=1, color=df['species'])
fig = px.scatter(projection, x='PC1', y='PC2', color='clusters', opacity=0.5)
for i, feature in enumerate(f):
    fig.add_shape(
        type='line',
        x0=0, y0=0,
        x1=loadings1[i, 0],
        y1=loadings1[i, 1],

    )
    fig.add_annotation(
        x=loadings1[i, 0],
        y=loadings1[i, 1],
        ax=0, ay=0,
        xanchor="center",
        yanchor="bottom",
        text=feature,
         font=dict(
                color="black",
                size=12
            )
    )
fig.show()


# In[16]:


projection.head()


# In[17]:


df_projection=dfff.merge(projection, on = ['id', 'name'])
dff_projection=df_projection.groupby('clusters').mean().reset_index(drop=False)


# In[18]:


fig = px.bar(dff_projection, x='clusters', y=['instrumentalness', 'energy', 'danceability', 'acousticness', 'valence', 'liveness', 'speechiness'], barmode='group')
fig.show()


# In[19]:


X.head()
X_df=X.copy()
#X_df['id']=dff_projection['id']
#X_df['name']=dff_projection['name']
X_df['clusters']=projection['clusters']
X_df.head()


# In[20]:


X_dff=X_df.groupby('clusters').mean().reset_index(drop=False)


# In[21]:


fig = px.bar(X_dff, x='clusters', y=['instrumentalness', 'energy', 'danceability', 'acousticness', 'valence', 'tempo', 'loudness', 'speechiness', 'liveness'], barmode='group')
fig.show()


# In[ ]:




