from db.loadmovie import LoadMovie
from decorators.retry import retry

import os
import json
import urllib2

def main():
    paths = ["lib/db/movies"]

    movie_info_url = "http://api.rottentomatoes.com/api/public/v1.0/movies/%s.json?apikey=mz7z7f9zm79tc3hcaw3xb85w"
    movie_cast_url =  "http://api.rottentomatoes.com/api/public/v1.0/movies/%s/cast.json?apikey=mz7z7f9zm79tc3hcaw3xb85w"
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
                # Data Pre-Processing
                mpaa_rating = process_mpaa_rating(movie)
                theater_date, dvd_date = process_date(movie) 

                # Insert Movie
                print "Trying to add %s..." % movie['title']
                try:
                    instance = LoadMovie(
                        title=movie['title'],
                        mpaa_rating=mpaa_rating,
                        runtime=movie['runtime'],
                        critic_score=movie['ratings']['critics_score'],
                        synopsis=movie['synopsis'],
                        theater_date=theater_date,
                        dvd_date=dvd_date
                    )

                    # Insert Genres, Directors, Actors, and Images
                    movie_url = movie_info_url % movie[ 'id' ]
                    movie_profile = call_api(movie_url)
                    instance.insert_genres(movie_profile['genres'])
                    directors = process_cast(
                        movie_profile['abridged_directors'])
                    instance.insert_directors(directors)

                    cast_url = movie_cast_url % movie[ 'id' ]
                    movie_cast = call_api(cast_url)
                    actors = process_cast(movie_cast['cast'])
                    instance.insert_actors(actors)
                    
                    image_url = movie['posters']['original']
                    instance.insert_image(image_url)

                except Exception, e:
                    print e
                    continue

def process_mpaa_rating(movie):
    if movie['mpaa_rating'] == 'Unrated':
        return 'NR'
    else:
        return movie['mpaa_rating']

def process_cast(cast):
    return [c['name'] for c in cast]

def process_date(movie):
    DEFAULT_DATE = "9999-12-31"
    if movie['release_dates'].has_key('theater'):
        theater_date = movie['release_dates']['theater']
    else:
        theater_date = DEFAULT_DATE
    if movie['release_dates'].has_key('dvd'):
        dvd_date = movie['release_dates']['dvd']
    else:
        dvd_date = DEFAULT_DATE
    return (theater_date, dvd_date)

@retry(urllib2.HTTPError)
def call_api(url):
    response = urllib2.urlopen(url)
    return json.loads(response.read())

if __name__ == "__main__":
    main()
