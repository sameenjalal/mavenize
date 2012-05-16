import datetime
from haystack import indexes
from apps.movie.models import Movie

class MovieIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    cast = indexes.CharField(model_attr='cast')
    directors = indexes.CharField(model_attr='directors')

    def get_model(self):
        return Movie

    def index_queryset(self):
        return self.get_model().objects.all()
