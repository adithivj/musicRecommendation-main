
import requests
import json
import pandas as pd
from pathlib import Path

#TODO Change your input json file location
f = open('/Users/mkoh/Documents/GeorgiaTechMaster/Fall2022/CS6242_GroupProject/TODO/100000_to_102000.json')
data = json.load(f)


#print(data)

playcount = []
listeners = []
artist = []
trackname = []

for i in data:
    if 'track' in i.keys():
        artist.append(i['track']['artist']['name'])
        trackname.append(i['track']['name'])
        playcount.append(i['track']['playcount'])
        listeners.append(i['track']['listeners'])
    else:
        artist.append('NA')
        trackname.append('NA')
        playcount.append('NA')
        listeners.append('NA')

print('Done')


tmp = pd.DataFrame(list(zip(artist,trackname,playcount,listeners)), columns = ['artist','trackname','playcount','listeners'])
filepath = Path('100000_to_102000.csv')  #TODO - Update the output file name to your rows
filepath.parent.mkdir(parents=True, exist_ok=True)
tmp.to_csv(filepath)
