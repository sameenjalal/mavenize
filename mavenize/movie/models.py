from django.db import models
from django.template.defaultfilters import slugify

class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    synopsis = models.TextField()
    release_date = models.DateField(auto_now=False)
    image = models.ImageField(upload_to='img/movies')
    awards = models.TextField()
    cast = models.TextField()
    directors = models.TextField()
    similars = models.TextField()
    url = models.SlugField()

    def __unicode__(self):
        return "%s: %s" % (self.movie_id, self.title)

    def save(self, *args, **kwargs):
		if not self.movie_id:
			self.url = slugify(self.title)
		super(Movie, self).save(*args, **kwargs)
