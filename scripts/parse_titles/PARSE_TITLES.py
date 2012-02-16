import json
json_data=open('titles.json')
data = json.load(json_data)

for x in data['catalog_titles']:
    print x

json_data.close()
