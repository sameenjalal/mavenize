import json
from pprint import pprint

json_data=open('Genres.json')
data = json.load(json_data)

for x in data['d']:
    print x['Name']

json_data.close()
