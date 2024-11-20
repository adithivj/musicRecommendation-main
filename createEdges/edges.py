import pandas as pd
import csv

df = pd.read_csv('tracks_final_dataset.csv')

artists = df[['artist1','associatedArtist1','associatedArtist2','associatedArtist3']]

artists_limited = artists.iloc[:30000]

edge = []
for index, row in artists_limited.iterrows():
    if not pd.isnull(row['associatedArtist1']):
        pair = tuple([row['artist1'], row['associatedArtist1']])
        edge.append(pair)
    if not pd.isnull(row['associatedArtist2']):
        pair2 = tuple([row['artist1'], row['associatedArtist2']])
        edge.append(pair2)
    if not pd.isnull(row['associatedArtist3']):
        pair3 = tuple([row['artist1'], row['associatedArtist3']])
        edge.append(pair3)


with open('edge.csv','w') as out:
    csv_out = csv.writer(out)
    csv_out.writerow(['artist1', 'artist2'])
    for row in edge:
        csv_out.writerow(row)