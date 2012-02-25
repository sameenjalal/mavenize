import os
import fileinput
import json

path = 'data_files_from_tmdb/'
listing = os.listdir(path)

i = 0
for infile in listing:
    #print "current file is: " + infile + ": " + str(i)
    file_path = path + infile
    json_file = open( file_path, "r" ).read()
    json_data = json.loads( json_file )
    for line in json_data:
        try:
            for key,val in line.iteritems():
                if key == "id":
                    print infile.strip( ".json" ) + ":" + str( val )
        except:
            pass
