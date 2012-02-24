from apps.movie.models import Movie

def get_cast():
    movies = Movie.objects.all()
    
    for movie in movies:
        #movie.cast = fetchcast()
        #movie.directors = fetchdirector()
        movie.save()
