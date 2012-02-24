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

