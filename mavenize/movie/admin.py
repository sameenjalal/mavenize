from django.contrib import admin
from mavenize.movie.models import Movie
from mavenize.movie.models import Genre

admin.site.register(Movie)
admin.site.register(Genre)

class MovieAdmin(admin.ModelAdmin):
	prepopulated_fields = {"url": ("title",)}
