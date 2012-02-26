import urllib
import json
import fileinput

url = "http://api.themoviedb.org/3/movie/%s/casts?api_key=c3648d284b99debdb865cf318248b209"

table_name = "movie_movie"
cast_sql = "UPDATE " + table_name + " SET casts='%s' WHERE title LIKE '%s';"
dir_sql = "UPDATE " + table_name + " SET directors='%s' WHERE title LIKE '%s';"

data_file = "NAME_TMDBNAME_TMDBID.txt"
i = 0
for line in fileinput.input( data_file ):
    line = line.strip()
    args = line.split( ":::" )

    my_title = args[0].replace( " " , "_" )
    tmdb_title = args[1].replace( " " , "_" )
    tmdb_id = args[2]

    dl_url = url % tmdb_id
    print dl_url + " -O info_tmdb/" + my_title + "___" + tmdb_title
