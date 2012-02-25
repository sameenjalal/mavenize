from django.core.files.base import ContentFile
from apps.movie.models import Movie

from urllib2 import urlopen, HTTPError

def get_image():
    movies = Movie.objects.all()

    for movie in movies:
        #fetch the url
        #url = fetchurl(movie.title)
        img = urlopen(url,timeout=30)
        movie.image.save(movie.url+u'.jpg', ContentFile(img.read()))

def fetchurl( title ):
	url_file = "TITLE_COLON_IMG_URL.txt"
	for line in open(url_file,'r').readlines():
		val = line.split( ":" , 1 )
		if val[0] == title:
			return val[1]
	return "Nothing"
