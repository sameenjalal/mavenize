import tmdb
import pprint


tmdb.configure( "c3648d284b99debdb865cf318248b209" )
movie = tmdb.Movie("Living Legends of Comedy: Real Talk")
credits = tmdb.Credits("Living Legends of Comedy: Real Talk")

movie_id = movie.get_id()

print movie.full_info( movie_id )
print movie.get_total_results()
"""
print movie.is_adult()
print movie.get_genres( movie_id )
print movie.get_collection_name( movie_id )
print movie.get_overview( movie_id )
print
print credits.get_cast_id()
print credits.get_cast_character()
"""
