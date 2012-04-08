import json
from django.utils.encoding import smart_str, smart_unicode
from django.template.defaultfilters import slugify

for file_num in range( 0, 58 ):
    json_file_name = "titles/" + str(file_num) + "_titles.json"
    json_data=open( json_file_name )
    data = json.load(json_data)

    #print data['catalog_titles']['catalog_title'][0].keys()

    try:
        for item in range(0,len(data['catalog_titles']['catalog_title'])):
            title = str(data['catalog_titles']['catalog_title'][item]['title']['regular'])
            title = title.replace( "'", "''")
            title = title.replace( "\"", "''" )
            title = title.replace( "\"", "''" )
            title = title.replace( ".", "" )

            all_genres = []
            for x in data['catalog_titles']['catalog_title'][item]['category']:
                try:
                    if x:
                        all_genres.append( x['term'] )
                        #print x['term']
                except:
                    all_genres.append( x )
                    #print x
                    pass
            #print all_genres

            # Now sql statement to add all genres for every title
            values_stmt = "'"
            for genre in all_genres:
                genre = genre.replace( "'", "''")
                genre = genre.replace( "\"", "''" )
                genre = genre.replace( "\"", "''" )
                genre = genre.replace( ".", "" )

                values_stmt1 = "SELECT movie_id from movie_movie WHERE title='%s' LIMIT 1" % title
                values_stmt2 = "SELECT id from movie_genre WHERE name='%s' LIMIT 1" % genre

                overarching = "INSERT INTO movie_movie_genre ( movie_id, genre_id ) VALUES ( (%s), (%s) );" % (values_stmt1, values_stmt2)
                print overarching

            #break
        #break
    except:
        print "=======================BEGIN fucked up====================="
        print item
        print "=======================END fucked up======================="
        raise

    json_data.close()

#print smart_str(huge_genre_set)
#print
