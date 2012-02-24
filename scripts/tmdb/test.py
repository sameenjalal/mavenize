import tmdb
import pprint


tmdb.configure( "c3648d284b99debdb865cf318248b209" )
o = 0
try:
    for line in open('all_titles_from_psql.txt','r'):
        line = line.strip()
        movie = tmdb.Movie( line )

        movie_id = movie.get_id()
        title_poster = {"title": line, "poster": movie.get_poster()}
        o += 1
        if o > 5:
            break
except: pass
print title_poster


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
