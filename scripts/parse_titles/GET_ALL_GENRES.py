import json
from django.utils.encoding import smart_str, smart_unicode
from django.template.defaultfilters import slugify

huge_genre_set = set()
for file_num in range( 0, 58 ):
    json_file_name = "titles/" + str(file_num) + "_titles.json"
    json_data=open( json_file_name )
    data = json.load(json_data)

    #print data['catalog_titles']['catalog_title'][0].keys()

    try:
        for item in range(0,len(data['catalog_titles']['catalog_title'])):
            title = data['catalog_titles']['catalog_title'][item]['title']['regular']
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

            # Starting to generate insert statements for fields and values
            table_name = "movie_genre"
            values_stmt = "'"

            for genre in all_genres:
                genre = genre.replace( "'", "''")
                genre = genre.replace( "\"", "''" )
                genre = genre.replace( "\"", "''" )
                genre = genre.replace( ".", "" )
                huge_genre_set.add( genre )

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
table_name = "movie_genre"
stmt = "INSERT INTO " + table_name + " ( name, url ) VALUES ( '%s', '%s' );"
for x in huge_genre_set:
    print stmt % (x, slugify(x))
