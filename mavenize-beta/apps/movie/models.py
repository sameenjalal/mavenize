from django.db import models
from django.template.defaultfilters import slugify
from item.models import Item
from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.dispatch import receiver

class Genre(models.Model):
    name = models.CharField(max_length=50)
    url = models.SlugField(null=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.url = slugify(self.name)
        super(Genre, self).save(*args, **kwargs)

class Actor(models.Model):
    name = models.CharField(max_length=50)
    url = models.SlugField(null=True)
    
    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.url = slugify(self.name)
        super(Actor, self).save(*args, **kwargs)

class Director(models.Model):
    name = models.CharField(max_length=50)
    url = models.SlugField(null=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.url = slugify(self.name)
        super(Director, self).save(*args, **kwargs)

class Movie(models.Model):
    item = models.OneToOneField(Item, primary_key=True)
    title = models.CharField(max_length=60)
    mpaa_rating = models.CharField(max_length=5)
    runtime = models.SmallIntegerField()
    critic_score = models.SmallIntegerField()
    genre = models.ManyToManyField(Genre)
    synopsis = models.TextField()
    theater_date = models.DateField(null=True)
    dvd_date = models.DateField(null=True)
    image = models.ImageField(
        upload_to='img/movies',
        default='img/movies/default.jpg'
    )
    directors = models.ManyToManyField(Director)
    actors = models.ManyToManyField(Actor)
    url = models.SlugField(null=True)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.item:
            self.url = slugify(self.title)
        super(Movie, self).save(*args, **kwargs)

    # Need to implement permalink

"""
Saves the item when using the following command:
Movie.objects.create(item=Item(),...)
"""
@receiver(post_save, sender=Movie)
def create_movie(sender, instance, created, **kwargs):
    if created:
        instance.item.save()

@receiver(post_delete, sender=Movie)
def delete_movie(sender, instance, **kwargs):
    Item.objects.get(pk=instance.pk).delete()
