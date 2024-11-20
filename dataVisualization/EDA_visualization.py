#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')
df=pd.read_csv("tracks_final_dataset_genres_encoded_new.csv")
df.head(5)
feature=df.select_dtypes(np.number).columns.tolist()[2:]
#print(features)
fea=['key', 'mode', 'time_signature', 'explicit'] 
#'popularity', 'explicit', 'liveness', 'loudness']
#features=[f for f in feature if f not in fea]
features=['popularity',
 'duration_ms',
 'danceability',
 'energy',
 'loudness',
 'speechiness',
 'acousticness',
 'instrumentalness',
 'liveness',
 'valence',
 'tempo']
df1=df[features+['playcount', 'listeners']]
ddf1=df[fea]

#df0_df1=df[features+['release_date', 'genres']]
df0_df1=df[features+['release_date', 'genres', 'playcount', 'listeners']]
#features
df0_df1['genre']=df0_df1['genres'].apply(lambda x: eval(x)[0])
df0=df0_df1[['release_date', 'genre', 'playcount', 'listeners']]
#df0_df1
#df.head(5)


# In[2]:


df1['release_date']=pd.to_datetime(df['release_date'])
df1['year'] = pd.DatetimeIndex(df['release_date']).year
df1.head()


# In[3]:


df0['release_date']=pd.to_datetime(df0['release_date'])
df0['year'] = pd.DatetimeIndex(df0['release_date']).year
#df0.head()


# In[4]:


df0_df1['release_date']=pd.to_datetime(df0_df1['release_date'])
df0_df1['year'] = pd.DatetimeIndex(df0_df1['release_date']).year
df0_df1.head()


# In[5]:


#[reference:https://careerfoundry.com/en/blog/data-analytics/how-to-find-outliers/]
def find_outliers_IQR(df):

    q1=df.quantile(0.25)

    q3=df.quantile(0.75)

    IQR=q3-q1

    outliers = df[((df<(q1-1.5*IQR)) | (df>(q3+1.5*IQR)))]
  
    return outliers

outliers = find_outliers_IQR(df1['duration_ms'])


# In[6]:


dff_copy=df1.copy()
dfff=dff_copy.drop(outliers.index, axis=0).reset_index(drop=True)
dff_c=dfff[dfff.columns[2:11]]
#dff_c


# In[7]:


##[reference: https://www.geeksforgeeks.org/how-to-create-a-triangle-correlation-heatmap-in-seaborn-python/]
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(rc = {'figure.figsize':(16,8)})
mask=np.triu(np.ones_like(dff_c.corr(), dtype=np.bool))
ax = sns.heatmap(dff_c.corr(), mask=mask, annot=True, cmap='BrBG')
ax.set_title('Audio Features Triangle Correlation Heatmap', fontdict={'fontsize':18}, pad=12)
plt.show()


# In[8]:


df0_copy=df0.copy()
dff0=df0_copy.drop(outliers.index, axis=0).reset_index(drop=True)
#dff0.head()


# In[9]:


df0_df1_copy=df0_df1.copy()
df0f1=df0_df1_copy.drop(outliers.index, axis=0).reset_index(drop=True)
df0f1.head()
df0df1=df0f1.loc[df0f1['year']<=2020]
df0df1.head()


# In[10]:


#df1.info()
df2=dfff.groupby(['year']).mean()
df3=df2.loc[1922:2020, :]
df3=df3.reset_index(drop=False)
#df3.head()


# In[11]:



import collections
ddf2=dff0.groupby(['year'])['genre'].agg(pd.Series.mode).explode()

ddf3=ddf2.loc[1922:2020]
ddf3=ddf3.reset_index(drop=False)

genre_list=ddf3['genre'].to_list()

#genre_l=[]
#for g in genre_list:
    #if type(g)==str:
        #genre_l.append(g)
    #else:
        #genre_l.append(g[1])
#genre_l
counter = collections.Counter(genre_list)
counter
common=counter.most_common(4)
common

df_genre = pd.DataFrame(common, columns =['most frequent genre', 'count'])

df_genre


# In[12]:


yeardict={}
for c in (df_genre['most frequent genre'].to_list()):
    L=[]
    L=ddf3.loc[ddf3['genre']==c]['year'].to_list()
    yeardict[c]=str(min(L))+'-'+str(max(L))
#yeardict


# In[13]:


df_genre['year interval']=yeardict.values()

df_genre


# In[14]:


#ddff01=df0df1.groupby('genre')[features].mean().reset_index(drop=False)
ddff01=df0df1.groupby('genre')[features+['playcount', 'listeners']].mean().reset_index(drop=False)
#ddff01.nlargest(10, 'popularity')
df01=ddff01.loc[ddff01['genre'].isin(df_genre['most frequent genre'].to_list())]
#ddff01
df01=df01.rename(columns={'genre':'most frequent genre'})
df_genre=pd.merge(df_genre, df01[['most frequent genre', 'popularity', 'playcount', 'listeners']].reset_index(drop=True), how='inner')
df_genre['popularity']=round(df_genre['popularity'], 2)
df_genre['playcount']=round(df_genre['playcount'], 2)
df_genre['listeners']=round(df_genre['listeners'], 2)
df_genre['playcount_per_listener']=df_genre['playcount']/df_genre['listeners']
#df01[['most frequent genre', 'popularity']]
df_genre


# In[15]:


fig=px.bar(x=df_genre['most frequent genre'], y=df_genre['count'], text=df_genre['year interval'], labels=dict(x="genres appear the most", y="Count"))

#fig=px.scatter(x=df_genre['most frequent genre'], y=df_genre['popularity'], text=df_genre['popularity'])
#fig.add_bar(x=df_genre['most frequent genre'], y=df_genre['count'], text=df_genre['year interval'])
fig.show()


# In[16]:


fig = px.bar(df01, x='most frequent genre', y=['instrumentalness', 'energy', 'danceability', 'acousticness', 'valence', 'liveness', 'speechiness'], barmode='group')
fig.show()


# In[17]:


import plotly.express as px 
sound_features = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness']
fig = px.line(df3, x='year', y=sound_features)
fig.show()


# In[18]:


fig = px.line(df3, x='year', y='popularity')
fig.show()


# In[19]:


fig = px.line(df3, x='year', y='duration_ms')
fig.show()


# In[20]:


fig = px.line(df3, x='year', y='tempo')
fig.show()


# In[21]:


df3['playcount_per_listener']=df3['playcount']/df3['listeners']
fig = px.line(df3, x='year', y='playcount_per_listener')
fig.show()

