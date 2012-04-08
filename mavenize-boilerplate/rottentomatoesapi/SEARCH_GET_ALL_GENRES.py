import os
import json
import urllib2

paths = [ 'harry', 'heart', 'hotel', 'lawyer', 'list', 'lord', 'love', 'matrix', 'potter', 'ring', 'star', 'titanic', 'twilight', 'wars' ]
starting_path = "searches/"

path_id_to_genres = "id_to_genres/"
movie_info_url = "http://api.rottentomatoes.com/api/public/v1.0/movies/%s.json?apikey=mz7z7f9zm79tc3hcaw3xb85w"

for path in paths:
    path = starting_path + path
    dirList = os.listdir( path )
    for fn in dirList:
        json_file = open( path + "/" + fn ).read()
        json_data = json.loads( json_file )

        try:
            movies = json_data['movies']
        except:
            continue

        for movie in movies:
            if movie.has_key('alternate_ids'):
                movie.pop( 'alternate_ids' )
            if movie.has_key('critics_consensus'):
                movie.pop( 'critics_consensus' )
            if movie.has_key('mpaa_rating'):
                movie.pop( 'mpaa_rating' )
            if movie.has_key('links'):
                movie.pop( 'links' )
            if movie.has_key('runtime'):
                movie.pop( 'runtime' )
            if movie.has_key('ratings'):
                movie.pop( 'ratings' )

            """
            print movie.keys()
            print movie['title']
            print movie['release_dates']
            print movie['abridged_cast']
            print movie['synopsis']
            print movie['year']
            print movie['posters']
            print movie['id']
            """

            movie_url = movie_info_url % movie[ 'id' ]
            response = urllib2.urlopen( movie_url )
            json_html = json.loads( response.read() )

            genres = json_html[ 'genres' ]
            genres_json = json.dumps( genres )

            fp = open( path_id_to_genres + movie[ 'id' ], 'w' )
            fp.write( genres_json )
            fp.close()
