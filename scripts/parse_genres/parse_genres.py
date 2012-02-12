import json
from pprint import pprint

json_data=open('json_genres.json')
data = json.load(json_data)

for x in data['d']:
    print x['__metadata']['uri'] + "/Titles?$format=json"

json_data.close()
