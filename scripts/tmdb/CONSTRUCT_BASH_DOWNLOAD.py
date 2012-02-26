import tmdb
import pprint

tmdb.configure( "c3648d284b99debdb865cf318248b209" )

i = 0
url = "http://api.themoviedb.org/2.1/Movie.search/en/json/c3648d284b99debdb865cf318248b209/%s -O tmdb_files/%s.json"
for line in open('all_titles_from_psql.txt','r'):
	line = line.strip()
	line = line.strip()
	line_plus = line.replace( " " , "+" )
	line_underscore = line.replace( " " , "_" )

	print url % (line_plus, line_underscore)
