import json
import time

from flask import Flask, send_file, render_template, Response
import csv
from flask import request
from findSimilarity.NearestNeighborClassification import *

import pandas as pd

MAX_ROWS_TO_PARSE = 100000
DATASET_PATH = 'resources/FinalDataSet1/tracks_final_dataset_clustered_sample.csv'


genres = ["acoustic",
"afrobeat",
"alternative",
"ambient",
"anime",
"bluegrass",
"blues",
"brazil",
"breakbeat",
"british",
"children",
"chill",
"classical",
"club",
"comedy",
"country",
"dance",
"dancehall",
"disco",
"disney",
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
"hardcore",
"hardstyle",
"hip-hop",
"house",
"idm",
"indian",
"indie",
"industrial",
"j-idol",
"jazz",
"kids",
"latin",
"latino",
"malay",
"metal",
"metalcore",
"mpb",
"opera",
"pagode",
"party",
"piano",
"pop",
"punk",
"reggae",
"reggaeton",
"rock",
"rockabilly",
"romance",
"sad",
"salsa",
"samba",
"sertanejo",
"ska",
"sleep",
"songwriter",
"soul",
"spanish",
"swedish",
"tango",
"techno",
"trance",
"turkish"]


audio_features_df = loadData(DATASET_PATH)
audio_features_non_normalized_df = loadNonNormalized(DATASET_PATH)

audio_feature_df_dropped = drop_audio_features(audio_features_df)
song_features_df = audio_features_non_normalized_df[["id","name", "artists","duration_ms", 'key', 'mode', "release_date", "acousticness",'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness',  'speechiness', 'tempo', 'valence','playcount','listeners','genres']]

audio_features_df_label_0 =  audio_features_df[audio_features_df.clusters == 0]
audio_features_df_label_1 =  audio_features_df[audio_features_df.clusters == 1]
audio_features_df_label_2 =  audio_features_df[audio_features_df.clusters == 2]
audio_features_df_label_3 =  audio_features_df[audio_features_df.clusters == 3]
audio_features_df_label_4 =  audio_features_df[audio_features_df.clusters == 4]

audio_features_df_dropped_label_0 =  drop_audio_features(audio_features_df_label_0)
audio_features_df_dropped_label_1 =  drop_audio_features(audio_features_df_label_1)
audio_features_df_dropped_label_2 =  drop_audio_features(audio_features_df_label_2)
audio_features_df_dropped_label_3 =  drop_audio_features(audio_features_df_label_3)
audio_features_df_dropped_label_4 =  drop_audio_features(audio_features_df_label_4)

audio_features_non_normalized_df_label_0 =  audio_features_non_normalized_df[audio_features_df.clusters == 0]
audio_features_non_normalized_df_label_1 =  audio_features_non_normalized_df[audio_features_df.clusters == 1]
audio_features_non_normalized_df_label_2 =  audio_features_non_normalized_df[audio_features_df.clusters == 2]
audio_features_non_normalized_df_label_3 =  audio_features_non_normalized_df[audio_features_df.clusters == 3]
audio_features_non_normalized_df_label_4 =  audio_features_non_normalized_df[audio_features_df.clusters == 4]

song_features_df_label_0 = audio_features_df_label_0[["id","name", "artists","duration_ms",  "release_date"]]
song_features_df_label_1 = audio_features_df_label_1[["id","name", "artists","duration_ms",  "release_date"]]
song_features_df_label_2 = audio_features_df_label_2[["id","name", "artists","duration_ms",  "release_date"]]
song_features_df_label_3 = audio_features_df_label_3[["id","name", "artists","duration_ms",  "release_date"]]
song_features_df_label_4 = audio_features_df_label_4[["id","name", "artists","duration_ms",  "release_date"]]

graph_songs = set()
app = Flask(__name__)

@app.route("/")
@app.route("/index")
def home():
    return render_template("index.html")

@app.route("/variability")
def variability():
    allRecommendedSongs = set()
    #allRecommendedSongs.update(graph_songs)
    allRecommendedSongs |= set(graph_songs)
    print(graph_songs)
    # recommended_songs_df = audio_feature_df_dropped[
    #     audio_feature_df_dropped['id'].isin(graph_songs)]
    # print()
    return render_template("variability.html", graph_songs=allRecommendedSongs)


@app.route("/get_recommended_songs")
def recommended_songs():
    recommended_songs = request.args.get('graph_songs')
    print(recommended_songs)
    print(recommended_songs)
    recommended_songs = recommended_songs.replace("{", "")
    print(recommended_songs)
    recommended_songs = recommended_songs.replace("}", "")
    print(recommended_songs)
    recommended_songs = recommended_songs.replace("'", "")
    print(recommended_songs)
    recommended_songs_list = recommended_songs.split(", ")
    print(recommended_songs_list)
    print("lenght of recommended lis  ",len(recommended_songs_list))
    recommended_songs = []
    recommended_songs_df = audio_features_non_normalized_df[
        audio_features_non_normalized_df['id'].isin(recommended_songs_list)]
    print("recommended_songs_df ",recommended_songs_df.shape)
    print("recommended_songs_df columns ", recommended_songs_df.columns)

    recommended_songs_df = recommended_songs_df[['name','id','danceability', 'energy', 'loudness','speechiness','acousticness','instrumentalness','liveness', 'valence','tempo','playcount','listeners',"genres"]] 
    # for index, row in recommended_songs_df.iterrows():
    #     recommended_songs.append({
    #         "name": row["name"],
    #         "id": row["id"],
    #         "danceability": row["danceability"],
    #         "loudness": row["loudness"]})
    for index, row in recommended_songs_df.iterrows():
        print("row ", row)
        print("recommended_songs ", recommended_songs)
        for column in recommended_songs_df.columns:
            if column != 'name' and column != 'id':
                recommended_songs.append({
                "name": row["name"],
                "id": row["id"],
                "type":column,
                "value": row[column]

                })
    graph_songs.clear()
    return Response(json.dumps(recommended_songs), status=200, mimetype="application/json")


"""
    Renders the template
"""
@app.route("/songs")
def list_songs():
    genre = request.args.get('genre')
    artistID = request.args.get('artistID')
    year = request.args.get('year')

    if (genre != None):
        uri = f'http://127.0.0.1:5000/api/getTop30ByGenre?genre={genre}'
        filterType='Genre'
    elif (artistID != None):
        uri = f'http://127.0.0.1:5000/api/getTop30ByArtist?artistID={artistID}'
        filterType='Artist'
    elif (year != None):
        uri = f'http://127.0.0.1:5000/api/getTop30ByDecade?year={year}'
        filterType='Release Date'
    else:
        uri='http://127.0.0.1:5000/api/songs'
        filterType='None'

    return render_template("songs.html", filterType=filterType, uri=uri)


@app.route("/song_graph")
def picked_song():
    songs = request.args.get('songIds')
    return render_template("song_graph.html", selectedSongs=songs)

# @app.route("/songs3/<result>")
# def picked_song(result):
#     print(result)
#     #songId = request.args.get('result')
#
#     return render_template("songs2.html", result = result)
"""
    API to describe song detail
"""
@app.route("/api/song")
def song():
    song_id = request.args.get('songId')
    song_details = song_features_df.loc[song_features_df['id'] == song_id]
    song_detail_json = json.loads(song_details.to_json(orient='records'))[0]
    return Response(json.dumps(song_detail_json), status=200, mimetype="application/json")

"""
    APIs that list out songs
"""



@app.route("/api/songs")
def songs():
    #Just a sample code feel free to replace logic
    songs_to_list = []
    with open(DATASET_PATH, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for index, row in enumerate(csvreader):
            if (len(songs_to_list) > 30) : break
            print(row)


            songs_to_list.append(
                {
                    "index" : index,
                    "songId" : row["id"],
                    "songName": row["name"],
                    "artists" : row["artists"],
                    "duration_ms" : row["duration_ms"],
                    "popularity" : float(row["popularity"]) ,
                    "genres": row["genres"],
                    "playcount" : row["playcount"],
                    "listeners" : row["listeners"],
                    "energy" : row["energy"],
                    "key" : row["key"],
                    "speechiness" : row["speechiness"],
                    "acousticness" : row["acousticness"],
                    "instrumentalness" : row["instrumentalness"],
                    "liveness" : row["liveness"],
                    "valence"  :row["valence"],
                    "tempo" : row["tempo"]
                }
            )
        return Response(json.dumps(songs_to_list), status=200, mimetype="application/json")

"""
    API to get genre options
"""
@app.route("/api/getGenreOptions")
def getGenreOptions():
    with open(DATASET_PATH, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        genres = set()
        for index, row in enumerate(csvreader):
            if (len(genres) > MAX_ROWS_TO_PARSE):
                break
            genreRow = row['genres']
            split = genreRow.replace('[', "").replace(']', "").replace("'", "").replace(" ", "").split(",")
            genres.update(split)

        return Response(json.dumps(list(genres)), status=200, mimetype="application/json")

"""
    API to get top 30 song by playcount of a genre
"""
@app.route("/api/getTop30ByGenre")
def getTop30ByGenre():
    genre = 'genre_' + request.args.get('genre')

    with open(DATASET_PATH, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        songs = []

        for index, row in enumerate(csvreader):
            if (genre not in row):
                break

            if (row[genre] == '1'):
                songs.append(
                {
                    "index" : index,
                    "songId" : row["id"],
                    "songName": row["name"],
                    "artists" : row["artists"],
                    "duration_ms" : row["duration_ms"],
                    "popularity" : row["popularity"] ,
                    "genres": row["genres"],
                    "playcount" : float(row["playcount"]),
                    "listeners" : row["listeners"],
                    "energy" : row["energy"],
                    "key" : row["key"],
                    "speechiness" : row["speechiness"],
                    "acousticness" : row["acousticness"],
                    "instrumentalness" : row["instrumentalness"],
                    "liveness" : row["liveness"],
                    "valence"  :row["valence"],
                    "tempo" : row["tempo"],
                    "release_date" : row['release_date']
                }
            )
        
        sortedByPlaycount = sorted(songs, key=lambda artist: artist['playcount'], reverse=True)
        results = sortedByPlaycount[:30]

    return Response(json.dumps(results), status=200, mimetype="application/json")

"""
    API to get release date options
"""
@app.route("/api/getReleaseDateOptions")
def getReleaseDateOptions():
    decades = [ '1900', '1910', '1920', '1930', '1940', '1950', '1960', '1970', '1980', '1990', '2000', '2010', '2020']    
    return Response(json.dumps(decades), status=200, mimetype="application/json")

"""
    API to get top 30 song by playcount of a decade/year
"""
@app.route("/api/getTop30ByDecade")
def getTop30ByDecade():
    minYear = int(request.args.get('year'))
    maxYear = minYear + 10

    with open(DATASET_PATH, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        songs = []
        for index, row in enumerate(csvreader):
            release_date = row['release_date']
            yearShort = int(release_date[-2:])
            if yearShort < 23:
                yearLong = yearShort + 2000
            else:
                yearLong = yearShort + 1900

            songs.append(
                {
                    "index" : index,
                    "songId" : row["id"],
                    "songName": row["name"],
                    "artists" : row["artists"],
                    "duration_ms" : row["duration_ms"],
                    "popularity" : row["popularity"] ,
                    "genres": row["genres"],
                    "playcount" : float(row["playcount"]),
                    "listeners" : row["listeners"],
                    "energy" : row["energy"],
                    "key" : row["key"],
                    "speechiness" : row["speechiness"],
                    "acousticness" : row["acousticness"],
                    "instrumentalness" : row["instrumentalness"],
                    "liveness" : row["liveness"],
                    "valence"  :row["valence"],
                    "tempo" : row["tempo"],
                    "release_date" : yearLong
                }
            )
        
        songsFilteredByDecade = list([])
    
        for s in songs:
            releaseDate = s['release_date']
            if (minYear <= releaseDate & releaseDate <= maxYear):
                songsFilteredByDecade.append(s)

        sortedByPlaycount = sorted(songsFilteredByDecade, key=lambda artist: artist['playcount'], reverse=True)
        results = sortedByPlaycount[:30]

    return Response(json.dumps(results), status=200, mimetype="application/json")

"""
    API to get top artist options. Tracks sorted by playcount and then top 30 unique artists are taken.
"""
@app.route("/api/getTopArtistOptions")
def getTopArtistOptions():
    with open(DATASET_PATH, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        allTrackInfo = []
        maxNumRows = 100
        for index, row in enumerate(csvreader):            
            allTrackInfo.append(
            {
                "artist": row["artists"],
                "artistID": row["artist1"],
                "playcount" : float(row["playcount"])
            })
            
        tic = time.perf_counter()
        sortedByPlaycount = sorted(allTrackInfo, key=lambda artist: artist['playcount'], reverse=True)
        toc = time.perf_counter()

        print(f"Finished sorting {maxNumRows} rows in {toc - tic:0.4f} seconds")
        artistOptions = set()

        for a in sortedByPlaycount:
            if (len(artistOptions) > 30) : break
            artistOptions.add((a['artist'], a['artistID']))

        return Response(json.dumps(list(artistOptions)), status=200, mimetype="application/json")

"""
    API to get top 30 song by playcount of an artist by artistID
"""
@app.route("/api/getTop30ByArtist")
def getTop30ByArtist():
    artistIDArg = request.args.get('artistID')
    with open(DATASET_PATH, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        artistSongs = []
        for index, row in enumerate(csvreader):
            print(row)
            if (row["artist1"] == artistIDArg):
                artistSongs.append(
                {
                    "index": index,
                    "songId": row["id"],
                    "songName": row["name"],
                    "artists": row["artists"],
                    "duration_ms": row["duration_ms"],
                    "popularity": int(row["popularity"]),
                    "playcount" : float(row["playcount"]) ,
                    "genres" : str(row["genres"]),
                    "listeners" : row["listeners"],
                   "energy" : row["energy"],
                   "key" : row["key"],
                    "loudness" : row["loudness"],
                    "mode" : row["mode"],
                    "speechiness" : row["speechiness"],
                    "acousticness" : row["acousticness"],
                    "instrumentalness" : row["instrumentalness"],
                     "liveness" : row["liveness"],
                     "valence" : row["valence"],
                     "tempo": row["tempo"]
                }
            )

        sortedSongs = sorted(artistSongs, key=lambda song: song['playcount'], reverse=True)
        results = sortedSongs[:30]

    return Response(json.dumps(results), status=200, mimetype="application/json")

# @app.route('/recommendedSongs/<song_dictionary>')
# def recommendedSongs(song_dictionary):
#     recommended_songs= []
#     recommended_df = getTop10Similar(song_dictionary, audio_features_df, audio_feature_df_dropped, song_features_df)
#     for index, row in recommended_df.iterrows():
#         recommended_songs.append(
#             {
#                 "Track name": row["name"],
#                 "artists": row["artists"],
#                 "duration_ms": row["duration_ms"],
#                 "Release Date": row["release_date"]
#             })
#     return Response(json.dumps(recommended_songs), status=200, mimetype="application/json")

## Add logic for top similar songs

def findTopSimilarSongs(selected_song, top_k) :
     songs = []
     songs.append(selected_song)
     #pd.set_option('max_columns', None)

     recommended_songs=[]
     recommended_df, recommendations = getTop10Similar(songs, audio_features_df, audio_feature_df_dropped, song_features_df, graph_songs)
     for index, row in recommended_df.iterrows():
        recommendation_row = recommended_df.loc[recommended_df['id'] == row["id"]].iloc[0]
        recommended_songs.append({
                 "name": row["name"],
                 "id": row["id"],
                 "duration_ms": row["duration_ms"],
                 "Release Date": row["release_date"],
                 "artists" : str(row["artists"]),
                 "genres" : str(row["genres"]),
                 "playcount": row["playcount"], 
                 "listeners" : row["listeners"],
                 "energy" : row["energy"],
                 "key" : row["key"],
                 "loudness" : row["loudness"], 
                 "mode" : row["mode"], 
                 "speechiness" : row["speechiness"], 
                 "acousticness" : row["acousticness"],
                 "instrumentalness" : row["instrumentalness"], 
                 "liveness" : row["liveness"], 
                 "valence" : row["valence"],
                 "tempo": row["tempo"]
        })
        graph_songs.add(row["id"])
     print(recommended_songs[0])
     return  recommended_songs[0:top_k]


def findTopSimilarSongs_clustered(selected_song, audio_features_input_clustered, audio_features_input_dropped_clusters,song_features_df_cluster, top_k):
    songs = []
    songs.append(selected_song)
    recommended_songs = []
    recommended_df, recommendations = getTop10Similar(songs, audio_features_df, audio_feature_df_dropped, song_features_df, graph_songs)
    for index, row in recommended_df.iterrows():
        recommendation_row = recommended_df.loc[recommended_df['id'] == row["id"]].iloc[0]
        recommended_songs.append({
                 "name": row["name"],
                 "id": row["id"],
                 "duration_ms": row["duration_ms"],
                 "Release Date": row["release_date"],
                 "artists" : str(row["artists"]),
                 "genres" : str(row["genres"]),
                 "playcount": row["playcount"], 
                 "listeners" : row["listeners"],
                 "energy" : row["energy"],
                 "key" : row["key"],
                 "loudness" : row["loudness"], 
                 "mode" : row["mode"], 
                 "speechiness" : row["speechiness"], 
                 "acousticness" : row["acousticness"],
                 "instrumentalness" : row["instrumentalness"], 
                 "liveness" : row["liveness"], 
                 "valence" : row["valence"],
                 "tempo": row["tempo"]
        })

        graph_songs.add(row["id"])

    return recommended_songs[0:top_k]

def recommend_cluster(selected_song) :
    song_list = []
    print(graph_songs)
    print("lenght of graph now ", len(graph_songs))
    song_details_cluster = audio_features_df.loc[song_features_df['id'] == selected_song]
    print("The cluster is ",  song_details_cluster["clusters"])
    if(song_details_cluster["clusters"].iloc[0] == 0):
        audio_features_input = audio_features_df_label_0
        audio_features_input_dropped = audio_features_df_dropped_label_0
        song_features_df_cluster =song_features_df_label_0
    elif (song_details_cluster["clusters"].iloc[0] == 1):
        audio_features_input = audio_features_df_label_1
        audio_features_input_dropped = audio_features_df_dropped_label_1
        song_features_df_cluster = song_features_df_label_1
    elif (song_details_cluster["clusters"].iloc[0] == 2):
        audio_features_input = audio_features_df_label_2
        audio_features_input_dropped = audio_features_df_dropped_label_2
        song_features_df_cluster = song_features_df_label_2
    elif (song_details_cluster["clusters"].iloc[0] == 3):
        audio_features_input = audio_features_df_label_3
        audio_features_input_dropped = audio_features_df_dropped_label_3
        song_features_df_cluster = song_features_df_label_3
    else:
        audio_features_input = audio_features_df_label_4
        audio_features_input_dropped = audio_features_df_dropped_label_4
        song_features_df_cluster = song_features_df_label_4
    top_similar_songs = findTopSimilarSongs_clustered(selected_song, audio_features_input,audio_features_input_dropped,song_features_df_cluster, 10)
    return top_similar_songs



def construct_response(selected_song, top_similar_sogs, algorithm_type) :

    song_details = audio_features_df.loc[audio_features_df['id'] == selected_song]
    song_detail_json = json.loads(song_details.to_json(orient='records'))[0]
    print("HIHIH")
    print(song_detail_json)
    response_template = {
      "nodes": [
        {"x": 452, "y": 410,"label":song_detail_json["name"], "id" : selected_song, "duration_ms" : song_detail_json["duration_ms"], "Release Date": song_detail_json["release_date"], "artists" :  song_detail_json["artists"], "genres" : song_detail_json["genres"], "playcount" : song_detail_json["playcount"], "listeners" :  song_detail_json["listeners"], "energy" : song_detail_json["energy"], "key" :  song_detail_json["key"], "loudness" : song_detail_json["loudness"], "mode" : song_detail_json["mode"], "speechiness" : song_detail_json["speechiness"], "acousticness" : song_detail_json["acousticness"], "instrumentalness" :  song_detail_json["instrumentalness"], "liveness" :  song_detail_json["liveness"], "valence" :  song_detail_json["valence"], "tempo" :  song_detail_json["tempo"]},
        {"x": 493, "y": 364, "label":"", "id" : ""},
        {"x": 442, "y": 365, "label":"", "id" : ""},
        {"x": 467, "y": 314, "label":"", "id" : ""},
        {"x": 477, "y": 248, "label":"", "id" : ""},
        {"x": 425, "y": 207, "label":"", "id" : ""},
        {"x": 402, "y": 155, "label":"", "id" : ""},
        {"x": 369, "y": 196, "label":"", "id" : ""},
        {"x": 350, "y": 148, "label":"", "id" : ""},
        {"x": 539, "y": 222, "label":"", "id" : ""},
         {"x": 539, "y": 222, "label":"", "id" : ""}

      ],
      "links": [
        {"source":  0, "target":  1},
        {"source":  0, "target":  2},
        {"source":  0, "target":  3},
        {"source":  0, "target":  4},
        {"source":  0, "target":  5},
        {"source":  0, "target":  6},
        {"source":  0, "target":  7},
        {"source":  0, "target":  8},
        {"source":  0, "target":  9},
        {"source":  0, "target":  10}
      ]
    }

    for index, top_song in enumerate(top_similar_sogs) :
        response_template["nodes"][index + 1]["label"] = top_song["name"]
        response_template["nodes"][index + 1]["id"] = top_song["id"]
        response_template["nodes"][index + 1]["duration_ms"] = top_song["duration_ms"]
        response_template["nodes"][index + 1]["Release Date"] =  top_song["Release Date"],
        response_template["nodes"][index + 1]["artists"]= top_song["artists"], 
        response_template["nodes"][index + 1]["genres"] = top_song["genres"],
        response_template["nodes"][index + 1]["playcount"]=top_song["playcount"], 
        response_template["nodes"][index + 1]["listeners"]= top_song["listeners"],
        response_template["nodes"][index + 1]["energy"]=top_song["energy"],
        response_template["nodes"][index + 1]["key"]= top_song["key"],
        response_template["nodes"][index + 1]["loudness"]=top_song["loudness"], 
        response_template["nodes"][index + 1]["mode"]=top_song["mode"], 
        response_template["nodes"][index + 1]["speechiness"]=top_song["speechiness"], 
        response_template["nodes"][index + 1]["acousticness"]=top_song["acousticness"],
        response_template["nodes"][index + 1]["instrumentalness"]= top_song["instrumentalness"], 
        response_template["nodes"][index + 1]["liveness"]= top_song["liveness"], 
        response_template["nodes"][index + 1]["valence"]= top_song["valence"],
        response_template["nodes"][index + 1]["tempo"]= top_song["tempo"]
    response_template["algorithm_type"] = algorithm_type
    return Response(json.dumps(response_template), status=200, mimetype="application/json")



@app.route('/api/recommendations')
def recommend() :
    song_list = []
    selected_song = request.args.get('selectedSong')
    algorithm_type = request.args.get('algorithm_type')

    if algorithm_type == "NearestNeighbor" : 
        top_similar_songs = findTopSimilarSongs(selected_song, 10)
    elif algorithm_type == "Cluster" :
        top_similar_songs = recommend_cluster(selected_song) 

    response = construct_response(selected_song, top_similar_songs, algorithm_type)
    return response


if __name__ == "__main__":
    app.run(debug=True)