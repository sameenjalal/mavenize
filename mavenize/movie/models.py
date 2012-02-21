from django.db import models
from django.template.defaultfilters import slugify

class Genre(models.Model):
    name = models.CharField(max_length=30)
    url = models.SlugField()

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.url = slugify(self.name)
        super(Genre, self).save(*args, **kwargs)

class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    genre = models.ManyToManyField(Genre, null=True)
    synopsis = models.TextField(null=True)
    release_date = models.TextField(null=True)
    image = models.ImageField(upload_to='img/movies', null=True)
    awards = models.TextField(null=True)
    cast = models.TextField(null=True)
    similars = models.TextField(null=True)
    url = models.SlugField(null=True)

    def __unicode__(self):
        return "%s: %s" % (self.movie_id, self.title)

    def save(self, *args, **kwargs):
        if not self.movie_id:
            self.url = slugify(self.title)
        super(Movie, self).save(*args, **kwargs)

class MoviePopularity(models.Model):
    movie = models.OneToOneField(Movie)
    popularity = models.BigIntegerField()

    def __unicode__(self):
        return "%s: %s" % (self.movie.title, self.popularity)

    class Meta:
        ordering = ('-popularity',)
