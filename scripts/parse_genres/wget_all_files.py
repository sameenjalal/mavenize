import urllib

fp = open('genre_name_url.txt','r'):
for line in fp:
    split = line.split("|")
    #command = "curl `" + split[1].strip() + "` > " + split[0].replace(" ","")
    urllib.urlretrieve( split[1].strip() )
    #print command
    print split[0]
