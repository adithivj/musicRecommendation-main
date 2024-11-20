
import requests
import json
import pandas as pd

##### Get list of artist and track #####
# TODO - Change the name and location of your csv file
df = pd.read_csv('/Users/mkoh/Documents/GeorgiaTechMaster/Fall2022/CS6242_GroupProject/partx.csv')

artists = df[['name','artists']]
artists = artists.rename(columns={'name': 'track', 'artists': 'artist'})
print(len(df))
#clean data
artists['artist'] = artists['artist'].str.replace("[", "")
artists['artist'] = artists['artist'].str.replace("]", "")
artists['artist'] = artists['artist'].str.replace("'", "")
artists['artist'] = artists['artist'].str.replace('"', "")


#Create a dictionary of artist and track for API
row_list = []
for index, rows in artists.iterrows():
    my_list = [rows.artist, rows.track]
    row_list.append(my_list)

dict_list = []
for pair in row_list:
    dict = {}
    dict['artist']=pair[0]
    dict['track']=pair[1]
    dict_list.append(dict)

#NOTE - If you need to further chop up the csv file you can use chopped_list instead
#chopped_list = dict_list[xx:xx]

###################################################################

API_KEY = 'bfb4830ce0fed6e0ace0b7f80b3eee6a'
USER_AGENT = 'Dataquest'


def lastfm_get(payload):
    headers = {'user-agent': USER_AGENT}
    url = 'https://ws.audioscrobbler.com/2.0/'

    payload['api_key'] = API_KEY
    payload['format'] = 'json'
    payload['method'] = 'track.getInfo'
    payload['autocorrect'] = 1

    response = requests.get(url, headers=headers, params=payload)
    return response

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

responses= [] #Append json first

for pairs in dict_list:  #Replace dict_list with chopped list here if needed to
    r = lastfm_get(pairs).json()
    responses.append(r)


print('done with append')

with open("partx.json", "w") as final: #TODO Update the name of json to reflect your part
    json.dump(responses, final)


print('done with json dump')

print(len(responses))


##### If you need to join json files you can use this code #####

# files=['xxx.json','xxx.json','93246_to_100000.json']
#
# def merge_JsonFiles(filename):
#     result = list()
#     for f1 in filename:
#         with open(f1, 'r') as infile:
#             result.extend(json.load(infile))
#
#     with open('50001_to_100000.json', 'w') as output_file:
#         json.dump(result, output_file)
#
# merge_JsonFiles(files)