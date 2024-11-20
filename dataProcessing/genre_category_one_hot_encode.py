#Refereces :https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html
#from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import MultiLabelBinarizer
import pandas as pd;
from sklearn.compose import make_column_transformer


def split_genres(row):
    #print(type(row));
    #print(row)
    row = row.replace("[", "")
    row = row.replace("]", "")
    row = row.replace("'", "")
    row_list = row.split(", ")
    return row_list;

def filter_empty_list(row):
    if(len(row) == 1):
        if(not row[0]):
            return False
        else:
            return True
    elif(len(row)>0):
        return True
    else:
        return False

audio_features_df = pd.read_csv('../resources/FinalDataSet1/tracks_final_dataset.csv')



print(audio_features_df.columns)

print(audio_features_df["Unnamed: 0"].head(10))


audio_features_df['genres_list'] = audio_features_df['genres'].apply(lambda x: list(split_genres(x)))

print(audio_features_df.shape)

audio_features_df = audio_features_df[audio_features_df['genres_list'].apply(lambda x: filter_empty_list(x))]

# audio_features_df = audio_features_df[audio_features_df['genres_list'].str.len() != 0]
# new_audio_features_df =audio_features_df[audio_features_df.astype(str)['genres_list'] != '[]']
print("after filter", audio_features_df.shape)
# print(audio_features_df.dtypes)
#
# ohe = OneHotEncoder()
# transformed = ohe.fit_transform(audio_features_df[['genres_list']])
#
# print(transformed.toarray())
#
# print(ohe.categories_)
#
# audio_features_df[ohe.categories_[0]] = transformed.toarray()
#
# print(audio_features_df.head())
#
#
# audio_features_df.to_csv('../resources/FinalDataset1/track_final.csv')


mlb = MultiLabelBinarizer(sparse_output=True)

print("before join")

audio_features_df = audio_features_df.join(
            pd.DataFrame.sparse.from_spmatrix(
                mlb.fit_transform(audio_features_df.pop('genres_list')),
                index=audio_features_df.index,
                columns=mlb.classes_))

print("after join")
audio_features_df = audio_features_df.drop(['genres'], axis=1)

audio_features_df.to_csv('../resources/FinalDataset1/tracks_final_dataset_genres_encoded.csv')