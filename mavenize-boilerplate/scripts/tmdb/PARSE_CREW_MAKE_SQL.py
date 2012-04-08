import os
import json
from django.utils.encoding import smart_str

path = 'info_tmdb/'
ls = os.listdir( path )

table_name = "movie_movie"
cast_sql = "UPDATE " + table_name + " SET cast='%s' WHERE title LIKE '%s' OR title LIKE '%s';"
dir_sql = "UPDATE " + table_name + " SET directors='%s' WHERE title LIKE '%s' OR title LIKE '%s';"

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
        my_title = my_title.replace( "'", "''" )
        tmdb_title = fc[1].replace( "_" , " " )
        tmdb_title = tmdb_title.replace( "'" , "''" )

        json_data.pop( 'id' )
        cast = json_data['cast']
        crew = json_data['crew']

        dir_str = ""
        for x in crew:
            x.pop( 'department' )
            x.pop( 'profile_path' )
            x.pop( 'id' )
            if x[ 'job' ] == "Director":
                dir_str += x['name'] + ","
        dir_str = dir_str.strip( "," )
        dir_str = dir_str.replace( "'" , "''" )
        stmt = dir_sql % (dir_str, my_title, tmdb_title)
        print smart_str( stmt )

        cast_str = ""
        for x in cast:
            x.pop( 'profile_path' )
            x.pop( 'id' )
            cast_str += x['name'] + ","
        cast_str = cast_str.strip( "," )
        cast_str = cast_str.replace( "'" , "''" )
        stmt = cast_sql % (cast_str, my_title, tmdb_title)
        #print smart_str( stmt )
except:
    raise
