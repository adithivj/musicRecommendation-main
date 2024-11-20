import pandas as pd

from sklearn.preprocessing import MultiLabelBinarizer

audio_features_df = pd.read_csv('../resources/FinalDataSet1/tracks_final_dataset_genres_encoded.csv')

mlb = MultiLabelBinarizer(sparse_output=True)

print("before join")

audio_features_df = audio_features_df.join(
            pd.DataFrame.sparse.from_spmatrix(
                mlb.fit_transform(audio_features_df.pop('key')),
                index=audio_features_df.index,
                columns=mlb.classes_).add_prefix('key_'))

print("after join")
audio_features_df.to_csv('../resources/FinalDataset1/tracks_final_dataset_genres_encoded.csv')