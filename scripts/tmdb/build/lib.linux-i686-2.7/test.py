import tmdb

tmdb.configure( "c3648d284b99debdb865cf318248b209" )
movie = tmdb.Movie("Alien")
print movie.get_id()

print movie.full_info(movie_id)
print movie.is_adult()
