from django.contrib import admin
from mavenize.movie.models import Movie
from mavenize.movie.models import Genre
from mavenize.movie.models import MoviePopularity

admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(MoviePopularity)

class MovieAdmin(admin.ModelAdmin):
    prepopulated_fields = {"url": ("title",)}
