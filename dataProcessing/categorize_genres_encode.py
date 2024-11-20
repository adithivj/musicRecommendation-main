import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer

genres_seeds =  [ "acoustic",   "afrobeat",  "alt-rock",
    "alternative",   "ambient",  "anime", "black-metal",  "bluegrass",   "blues",   "bossanova",   "brazil",
                 "breakbeat",   "british",    "cantopop",   "chicago-house",   "children", "chill",  "classical",  "club",
    "comedy",
    "country",
    "dance",
    "dancehall",
    "death-metal",
    "deep-house",
    "detroit-techno",
    "disco",
    "disney",
    "drum-and-bass",
    "dub",
    "dubstep",
    "edm",
    "electro",
    "electronic",
    "emo",
    "folk",
    "forro",
    "french",
    "funk",
    "garage",
    "german",
    "gospel",
    "goth",
    "grindcore",
    "groove",
    "grunge",
    "guitar",
    "happy",
    "hard-rock",
    "hardcore",
    "hardstyle",
    "heavy-metal",
    "hip-hop",
    "holidays",
    "honky-tonk",
    "house",
    "idm",
    "indian",
    "indie",
    "indie-pop",
    "industrial",
    "iranian",
    "j-dance",
    "j-idol",
    "j-pop",
    "j-rock",
    "jazz",
    "k-pop",
    "kids",
    "latin",
    "latino",
    "malay",
    "mandopop",
    "metal",
    "metal-misc",
    "metalcore",
    "minimal-techno",
    "movies",
    "mpb",
    "new-age",
    "new-release",
    "opera",
    "pagode",
    "party",
    "philippines-opm",
    "piano",
    "pop",
    "pop-film",
    "post-dubstep",
    "power-pop",
    "progressive-house",
    "psych-rock",
    "punk",
    "punk-rock",
    "r-n-b",
    "rainy-day",
    "reggae",
    "reggaeton",
    "road-trip",
    "rock",
    "rock-n-roll",
    "rockabilly",
    "romance",
    "sad",
    "salsa",
    "samba",
    "sertanejo",
    "show-tunes",
    "singer-songwriter",
    "ska",
    "sleep",
    "songwriter",
    "soul",
    "soundtracks",
    "spanish",
    "study",
    "summer",
    "swedish",
    "synth-pop",
    "tango",
    "techno",
    "trance",
    "trip-hop",
    "turkish",
    "work-out",
    "world-music"
]
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

def filter_empty(row):
    if not row:
        return False
    else:
        return True

def categorize(genre_list, unique_value_genres_map):
    new_genre_set=set()
    if genre_list:
        for genre in genre_list:
            if genre in unique_value_genres_map:
                new_genre_set.add(unique_value_genres_map.get(genre))
    return list(new_genre_set);


audio_features_df = pd.read_csv('../resources/FinalDataSet1/tracks_final_dataset.csv')

audio_features_df['genres_list'] = audio_features_df['genres'].apply(lambda x: list(split_genres(x)))
audio_features_df = audio_features_df[audio_features_df['genres_list'].apply(lambda x: filter_empty_list(x))]

unique_genres_map = {}
unique_value_genres_map ={}

unique_genres = audio_features_df["genres_list"].explode().unique()
unque_genre_set = set()
for genre_seed in genres_seeds:
    genres_classifcation_list =[]
    for unique_genre in unique_genres:
        if genre_seed in unique_genre:
            unque_genre_set.add(unique_genre)
            genres_classifcation_list.append(unique_genre)
            unique_value_genres_map[unique_genre] = genre_seed;
    if genres_classifcation_list:
        unique_genres_map[genre_seed] = genres_classifcation_list

print(unique_genres_map)

print(len(unique_genres))

print(len(unque_genre_set))

Difference = set(unique_genres) - unque_genre_set

print(Difference)

audio_features_df['genres_list'] = audio_features_df['genres_list'].apply(lambda x: list(categorize(x, unique_value_genres_map)))
audio_features_df = audio_features_df[audio_features_df['genres_list'].apply(lambda x: filter_empty(x))]
audio_features_df = audio_features_df.drop(['genres'], axis=1)

#df = pd.Series(sum([item for item in audio_features_df["genres_list"]], [])).value_counts()

mlb = MultiLabelBinarizer(sparse_output=True)

print("before join")

audio_features_df = audio_features_df.join(
            pd.DataFrame.sparse.from_spmatrix(
                mlb.fit_transform(audio_features_df.pop('genres_list')),
                index=audio_features_df.index,
                columns=mlb.classes_).add_prefix('genre_'))

print("after join")
audio_features_df.to_csv('../resources/FinalDataset1/tracks_final_dataset_genres_encoded.csv')
#print(df.head(10))





