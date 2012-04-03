from django.contrib import admin
from movie.models import Genre
from movie.models import Actor
from movie.models import Director
from movie.models import Movie

admin.site.register(Genre)
admin.site.register(Actor)
admin.site.register(Director)
admin.site.register(Movie)
