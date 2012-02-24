import tmdb
import pprint

tmdb.configure( "c3648d284b99debdb865cf318248b209" )

i = 0
for line in open('all_titles_from_psql.txt','r'):
	line = line.strip()
	line = line.strip()
	try:
		movie = tmdb.Movie( line )

		poster = movie.get_poster()
		title_poster = line + ":" + poster
		print title_poster
	except:
		pass

"""
print movie.full_info( movie_id )
print movie.get_total_results()
print movie.is_adult()
print movie.get_genres( movie_id )
print movie.get_collection_name( movie_id )
print movie.get_overview( movie_id )
print
print credits.get_cast_id()
print credits.get_cast_character()
"""
