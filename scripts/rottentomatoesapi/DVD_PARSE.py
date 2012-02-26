import os
import json

path="dvd"
dirList = os.listdir( path )
for fn in dirList:
    json_file = open( path + "/" + fn ).read()
    json_data = json.loads( json_file )

    print fn
    movies = json_data['movies']
    for movie in movies:
        if movie.has_key('alternate_ids'):
            movie.pop( 'alternate_ids' )
        if movie.has_key('critics_consensus'):
            movie.pop( 'critics_consensus' )
        print type(movie)
        print movie.keys()
        print movie['links']
    break
