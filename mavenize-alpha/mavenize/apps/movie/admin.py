from django.contrib import admin
from apps.movie.models import Movie
from apps.movie.models import Genre
from apps.movie.models import MoviePopularity

admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(MoviePopularity)

class MovieAdmin(admin.ModelAdmin):
    prepopulated_fields = {"url": ("title",)}
