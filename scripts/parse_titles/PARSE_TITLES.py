import json

for file_num in range( 0, 58 ):
    json_file_name = "titles/" + str(file_num) + "_titles.json"
    json_data=open( json_file_name )
    data = json.load(json_data)

#print data['catalog_titles']['catalog_title'][0].keys()

    try:
        for item in range(0,len(data['catalog_titles']['catalog_title'])):

            print "Title:"
            print data['catalog_titles']['catalog_title'][item]['title']['regular']
            print

            print "Netflix ID:"
            print data['catalog_titles']['catalog_title'][item]['id']
            print

            print "Genres:"
            for x in data['catalog_titles']['catalog_title'][item]['category']:
                try:
                    if x:
                        print x['term']
                except:
                    print x
                    pass
            print

            print "Release Year:"
            print data['catalog_titles']['catalog_title'][item]['release_year']
            print

            print "Image URL"
            print data['catalog_titles']['catalog_title'][item]['box_art']['large']
            print

            print "Average Rating"
            print data['catalog_titles']['catalog_title'][0]['average_rating']
            print

            for x in data['catalog_titles']['catalog_title'][item]['link']:
                for key,val in x.iteritems():
                    if key == "synopsis":
                        print "Synopsis"
                        print val
                        print
                    if key == "awards":
                        print "Awards:"
                        print val
                        print
                    if key == "catalog_titles":
                        print "Similars"
                        try:
                            a = val['link']
                        except:
                            print val
                            continue
                        for b in range( 0 , len( a )):
                            try:
                                print a[b]['title']
                            except:
                                try:
                                    for k,v in val['link'].iteritems():
                                        if k == "title":
                                            print v
                                except:
                                    print val
                                    pass
    except:
        print "fucked up"
        print item
        raise

    json_data.close()
