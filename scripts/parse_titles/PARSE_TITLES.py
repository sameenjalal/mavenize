import json
from django.utils.encoding import smart_str, smart_unicode

for file_num in range( 0, 58 ):
    json_file_name = "titles/" + str(file_num) + "_titles.json"
    json_data=open( json_file_name )
    data = json.load(json_data)

    #print data['catalog_titles']['catalog_title'][0].keys()

    try:
        for item in range(0,len(data['catalog_titles']['catalog_title'])):
            fields = []
            values = []

            #print "Title: format text"
            title = data['catalog_titles']['catalog_title'][item]['title']['regular']
            #print title
            fields.append( "title" )
            values.append( title )
            #print

            #print "Netflix ID: format text"
            #print data['catalog_titles']['catalog_title'][item]['id']
            #print

            #print "Genres: format list"
            """
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
            if all_genres:
                fields.append( "genre" )
                values.append( all_genres )
            #print
            """

            #print "Release Year: format text"
            release_date = data['catalog_titles']['catalog_title'][item]['release_year']
            fields.append( "release_date" )
            values.append( release_date )
            #print

            #print "Image URL: format text"
            pic = data['catalog_titles']['catalog_title'][item]['box_art']['large']
            # TODO: download pics and store it in db
            #print

            #print "Average Rating: format number"
            #print data['catalog_titles']['catalog_title'][0]['average_rating']
            #print

            for x in data['catalog_titles']['catalog_title'][item]['link']:
                for key,val in x.iteritems():
                    if key == "synopsis":
                        #print "Synopsis: format text"
                        #print val
                        fields.append( "synopsis" )
                        values.append( val )
                        #print
                    if key == "awards":
                        #print "Awards: format json list"
                        fields.append( "awards" )
                        values.append( val )
                        #print val
                        #print
                    if key == "catalog_titles":
                        #print "Similars: format list"
                        all_similars = []
                        try:
                            a = val['link']
                        except:
                            #print val
                            continue
                        for b in range( 0 , len( a )):
                            try:
                                all_similars.append( a[b]['title'] )
                                #print a[b]['title']
                            except:
                                try:
                                    for k,v in val['link'].iteritems():
                                        if k == "title":
                                            all_similars.append( v )
                                            #print v
                                except:
                                    #print val
                                    all_similars.append( val )
                                    pass
                        #print all_similars
                        if all_similars:
                            fields.append( "similars" )
                            values.append( all_similars )
            # First merge the two similar fields
            similars = []
            if fields and fields[-1] == "similars" and fields [-2] == "similars":
                similars += values.pop()
                similars += values.pop()
                fields.pop()
            values.append( similars )

            # Starting to generate insert statemetns for fields and values
            table_name = "movie_movie"
            values_stmt = "'"
            for fin in range( 0, len( fields ) ):
                item = values[ fin ]
                if not item:
                    fields.pop( fin )
                    continue
                #elif fields[ fin ] == "release_date":
                    #values_stmt = values_stmt[:-1] + str(item).replace( "'", "''") + ",\""
                elif isinstance( item , basestring ):
                    values_stmt += item.replace( "'", "''" ) + "','"
                else:
                    item = json.dumps( item ).replace( "'", "''")
                    item = item.replace( "\"", "''" )
                    values_stmt += item + "','"
            values_stmt = values_stmt.rstrip( "'" )
            values_stmt = values_stmt.strip( "," )
            values_stmt = values_stmt.replace( "." , "" )

            stmt = 'INSERT INTO %s (%s) VALUES (%s);' % (
                    table_name,
                    ','.join(fields),
                    values_stmt
                    )

            print smart_str(stmt)
            #f = open('1_netflix_sql.sql','w')
            #f.write( stmt )
            print
            #print values
            #break
        #break
    except:
        print "=======================BEGIN fucked up====================="
        print item
        print "=======================END fucked up======================="
        raise

    json_data.close()
