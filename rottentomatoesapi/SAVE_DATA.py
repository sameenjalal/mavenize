import os
import json
import urllib2

paths = [ "movies" , "dvd" ]

searchPath = "searches/"

searchList = os.listdir( searchPath )
for s in searchList:
    newSearchPath = searchPath + s + "/"
    paths.append( newSearchPath )

movie_info_url = "http://api.rottentomatoes.com/api/public/v1.0/movies/%s.json?apikey=mz7z7f9zm79tc3hcaw3xb85w"
for path in paths:
    dirList = os.listdir( path )
    for fn in dirList:
        json_file = open( path + "/" + fn ).read()
        json_data = json.loads( json_file )

        print fn
        if json_data.has_key( "error" ):
            print "continuing on: " + str(fn)
            continue
        movies = json_data['movies']
        for movie in movies:
            if movie.has_key('alternate_ids'):
                movie.pop( 'alternate_ids' )
            if movie.has_key('critics_consensus'):
                movie.pop( 'critics_consensus' )
            if movie.has_key('mpaa_rating'):
                movie.pop( 'mpaa_rating' )
            if movie.has_key('links'):
                movie.pop( 'links' )
            if movie.has_key('ratings'):
                movie.pop( 'ratings' )

            try:
                movie_url = movie_info_url % movie[ 'id' ]
                response = urllib2.urlopen( movie_url )
                json_html = json.loads( response.read() )
                genres = json_html[ 'genres' ]
                movie[ 'genres' ] = genres
            except:
                print movie_url
                continue

            ### Okay Dennis, at this point each movie object has these fields:
            # I'm not sure how to properly use the ORM in django to insert into
            # the db

            print movie.keys()
            print movie['title']
            print movie['release_dates']
            print movie['abridged_cast']
            print movie['synopsis']
            print movie['year']
            print movie['posters']
            print movie['id']
            print movie['genres']
            print movie['runtime']
            break
        break
