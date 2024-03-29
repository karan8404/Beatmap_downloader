import pickle
import requests
import math


def get_token():
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials',
        'scope': 'public'
    }

    response = requests.post(token_url, data=data)
    return response.json().get('access_token')


def get_beatmap_ids(limit, offset):
    global curr
    global to_download_mapsets
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    params = {
        'mode': 'osu',
        'offset': offset,
        'limit': limit,
    }

    response = requests.get(
        f'{api_url}/users/{player_id}/beatmapsets/{type}', headers=headers, params=params).json()

    for map in response:
        mapset_id = map['beatmapset']['id']
        if map['beatmap']['mode'] != 'osu' or mapset_id in to_download_mapsets.values():
            continue
        to_download_mapsets.update({curr: mapset_id})
        curr += 1


# setting up constants
api_url = 'https://osu.ppy.sh/api/v2'
token_url = 'https://osu.ppy.sh/oauth/token'

# Client information,Acticate by going to your osu account settings
client_id = 0 # Insert your client id here
client_secret = '' # Insert your client secret here
player_id = 0  # Insert Your player id here

# Type of beatmaps to download
# Go to https://osu.ppy.sh/docs/index.html#get-user-beatmaps for more options in type
#You may want to change line 37 and 38 depending on the structure of response recieved which changes based on type
type = "most_played"

# Number of beatmapsets to download
total = 100  # Insert the number of beatmapsets you want to download

token = get_token()

filepath = 'to_download_mapsets.pkl'
to_download_mapsets: dict = pickle.load(open(filepath, 'rb'))
curr = len(to_download_mapsets) + 1

for i in range(math.ceil(total/100)):
    offset = i*100
    limit = min(100, total-offset)
    get_beatmap_ids(limit, offset)

print("Mapsets to download: ", to_download_mapsets)
print("Number of Mapsets ", len(to_download_mapsets))
pickle.dump(to_download_mapsets, open(filepath, 'wb'))
