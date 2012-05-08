from movie.models import Movie
from haystack import indexes

import datetime

class MovieIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    genre = indexes.MultiValueField()
    actors = indexes.MultiValueField()
    directors = indexes.MultiValueField()
    release_date = indexes.DateTimeField(model_attr='theater_date')

    def get_model(self):
        return Movie

    def prepare_genre(self, obj):
        return [genre.name for genre in obj.genre.all()]

    def prepare_actors(self, obj):
        return [actor.name for actor in obj.actors.all()]

    def prepare_directors(self, obj):
        return [director.name for director in director.objects.all()]

    def index_queryset(self):
        return self.get_model().objects.all()
