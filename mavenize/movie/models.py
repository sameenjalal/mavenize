from django.db import models
from sorl.thumbnail import ImageField

class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    synopsis = models.TextField()
    release_date = models.DateTimeField(auto_now=False)
    image = models.ImageField(upload_to=None)
    awards = models.TextField()
    cast = models.TextField()
    directors = models.TextField()
    similars = models.TextField()

    def __unicode__(self):
        return "%s: %s" % (self.movie_id, self.title)
