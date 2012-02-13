import json
json_data=open('json_genres.json')
data = json.load(json_data)

for x in data['d']:
    print x['Name'] + "|" + x['__metadata']['uri'] + "/Titles?$format=json"

json_data.close()
