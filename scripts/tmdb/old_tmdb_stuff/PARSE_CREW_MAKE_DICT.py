import os
import json

path = 'info_tmdb/'
ls = os.listdir( path )

table_name = "movie_movie"
cast_sql = "UPDATE " + table_name + " SET cast='%s' WHERE title LIKE '%s';"
dir_sql = "UPDATE " + table_name + " SET directors='%s' WHERE title LIKE '%s';"

i = 0
try:
    for f in ls:
        file_path = path + f
        json_file = open( file_path, "r" ).read()
        try:
            json_data = json.loads( json_file )
        except:
            json_data = json.loads( "{ \"id\": 74256, \"cast\": [ { \"id\": 76215, \"name\": \"Adrian Lester\", \"character\": \"Richard\", \"order\": 0, \"profile_path\": \"/oeTSuzejXQ6vpzKdLRFO2SHiLXp.jpg\" }, { \"id\": 57449, \"name\": \"Jodhi May\", \"character\": \"Lelia\", \"order\": 1, \"profile_path\": \"/tjCdQybGCX7CHu9FojMq3l28dl6.jpg\" }, { \"id\": 20699, \"name\": \"Anamaria Marinca\", \"character\": \"Sylvie\", \"order\": 2, \"profile_path\": null } ], \"crew\": [ { \"id\": 84552, \"name\": \"RoryKelly\", \"department\": \"Directing\", \"job\": \"Director\", \"profile_path\": null } ] }" )

        fc = f.split( "___" )
        my_title = fc[0].replace( "_" , " " )
        tmdb_title = fc[1].replace( "_" , " " )

        json_data.pop( 'id' )
        cast = json_data['cast']
        crew = json_data['crew']

        for x in crew:
            x.pop( 'department' )
            x.pop( 'profile_path' )
            x.pop( 'id' )

        for x in cast:
            x.pop( 'profile_path' )
            x.pop( 'id' )

        print json_data
except:
    raise
