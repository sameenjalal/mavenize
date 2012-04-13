from urllib2 import urlopen, HTTPError
from django.template.defaultfilters import slugify
from django.core.files.base import ContentFile
from item.models import Item
import movie.models

class MovieDatabaseManager():
    actors = []
    directors = []
    genres = []
    movies = []

    def add_actor(actor_name):
        """
        Adds an actor to the list of actors.
        """
        actors.append(
            movie.models.Actor(
                name=actor_name,
                url=slugify(actor_name)
            )
        )

    def add_director(director_name):
        """
        Adds a director to the list of directors.
        """
        directors.append(
            movie.models.Director(
                name=director_name,
                url=slugify(director_name)
            )
        )

    def add_genre(genre_name):
        """
        Adds a genre to the list of genres.
        """
        genres.append(
            movie.models.Genre(
                name=genre_name,
                url=slugify(genre_name)
            )
        )

    def add_movie(title, mpaa_rating, runtime, critic_score, synopsis,
                  theater_date, dvd_date):
        """
        Adds a movie to the list of movies.
        """
        movies.append(
            movie.models.Movie(
                item=Item(),
                title=title,
                mpaa_rating=mpaa_rating,
                runtime=runtime,
                critic_score=critic_score,
                synopsis=synopsis,
                theater_date=theater_date,
                dvd_date=dvd_date,
                url=slugify(title)
            )
        )

    def insert_actors():
        """
        Inserts the actors list into the database.
        Precondition: The actors list is populated with Actor objects.
        """
        movie.models.Actor.objects.bulk_create(actors)

    def insert_directors():
        """
        Inserts the directors list into the database.
        Precondi2tion: The directors list is populated with Director
        objects.
        """
        movie.models.Director.objects.bulk_create(directors)

    def insert_genres():
        """
        Inserts the genres list into the database.
        Precondition: The genres list is populated with Genre objects.
        """
        movie.models.Genre.objects.bulk_create(genres)

    def insert_movies():
        """
        Inserts the movies list into the database.
        Precondition: The movies list is populated with Movie objects.
        """
        movie.models.Movie.objects.bulk_create(movies)

    def insert_movie_actors(title, theater_date, actor_list):
        """
        Inserts the actors for a given movie.
        actor_list is a list containing each actor's first and last
        name as one string.
        Precondition: The target movie and directors are already in
        the database.
        """
        actors = movie.models.Actor.objects.filter(name__in=actor_list)
        movie.models.Movie.objects.get(title=title,
            theater_date=theater_date).actors.add(*actors)

    def insert_movie_directors(title, theater_date, director_list):
        """
        Inserts the directors for a given movie.
        director_list is a list containing each director's first and
        last name as one string.
        Precondition: The target movie and directors are already in
        the database.
        """
        directors = movie.models.Director.objects.filter(
            name__in=director_list)
        movie.models.Movie.objects.get(title=title,
            theater_date=theater_date).directors.add(*directors)

    def insert_movie_genres(title, theater_date, genre_list):
        """
        Inserts the genres for a given movie.
        genre_list is the a list containing each genre's name as one
        string.
        Precondition: The target movie and genres are already in the
        database.
        """
        genres = movie.models.Genre.objects.filter(name__in=genre_list)
        movie.models.Movie.objects.get(title=title,
            theater_date=theater_date).genre.add(*genres)
    
    def insert_movie_image(title, theater_date, image_url):
        """
        Inserts the image for a given movie.
        Precondition: The target movie is already in the database.
        """
        image = urlopen(url, timeout=15)
        movie.models.Movie.objects.get(title=title,
            theater_date=theater_date).image.save(
                movie.url+u'.jpg',
                ContentFile(image.read())
            )
