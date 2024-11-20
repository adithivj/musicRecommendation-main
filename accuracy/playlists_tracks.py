import json;
import pandas as pd;
import os
dataset_df = pd.read_csv("/Users/pk/Learn/CSE-6242/workspace/CSE6242-project-team-16/resources/FinalDataSet1/tracks_final_dataset_clustered.csv")

path = "../resources/data"
dir_list = os.listdir(path)
i=0
for file in dir_list:
    print(file)
    with open(path + "/" + file) as json_file2:
        data = json.load(json_file2);
        i=i+1
        playlists = data['playlists'];

        playlist_df = pd.DataFrame(columns = ['playlist_name', 'track'])

#Iterate through list of dicts and generate a set with track uris

        track_uris = set()

        for playlist in playlists:
            tracks = playlist['tracks'];
            for track in tracks:
                #print(playlist["name"])
                #print(track["track_uri"])
                track=track["track_uri"].replace("spotify:track:","")
                x = track in dataset_df["id"].values
                if x:
                    playlist_df = playlist_df.append({'playlist_name': playlist["name"], 'track': track},
                           ignore_index=True)

        print("writing to dataframe")
        playlist_df.to_csv('../resources/FinalDataset1/playlist_tracks_'+str(i)+'.csv')








