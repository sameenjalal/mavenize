from django.contrib import admin
from mavenize.movie.models import Movie

admin.site.register(Movie)

class MovieAdmin(admin.ModelAdmin):
	prepopulated_fields = {"url": ("title",)}
