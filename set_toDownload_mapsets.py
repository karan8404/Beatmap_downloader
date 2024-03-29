# Set toDownload to maps mapset ids to download if not using get_mapset_ids.py
import pickle

filepath = 'to_download_mapsets.pkl'
# Insert the mapset ids you want to download here if not using get_mapset_ids.py
# Keep empty if you want to empty downloads queue
toDownload = []

dumpfile = {}
for i in range(len(toDownload)):
    dumpfile.update({i+1: toDownload[i]})

pickle.dump(dumpfile, open(filepath, 'wb'))
print("Mapsets to Download set to: ", pickle.load(open(filepath, 'rb')))
