from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

class Item(models.Model):
    five_star = models.IntegerField(default=0)
    four_star = models.IntegerField(default=0)
    three_star = models.IntegerField(default=0)
    two_star = models.IntegerField(default=0)
    one_star = models.IntegerField(default=0)
    bookmarks = models.IntegerField(default=0)
    bookmarks_active = models.IntegerField(default=0)

    def __unicode__(self):
        return str(self.id)

    def get_popularity(self):
        """
        Returns the Popularity model for this item.
        """
        if not hasattr(self, '_popularity_cache'):
            try:
                self._popularity_cache = Popularity.objects.get( 
                    item__id__exact=self.id)
                self._popularity_cache.item = self
            except:
                raise ObjectDoesNotExist 
        return self._popularity_cache

class Link(models.Model):
    item = models.ForeignKey(Item)
    partner = models.CharField(max_length=20)
    url = models.CharField(max_length=200)

    def __unicode__(self):
        return self.url

class Popularity(models.Model):
    item = models.OneToOneField(Item, primary_key=True)
    today = models.IntegerField(default=0, db_index=True)
    week = models.IntegerField(default=0, db_index=True)
    month = models.IntegerField(default=0, db_index=True)
    alltime = models.IntegerField(default=0, db_index=True)

    def __unicode__(self):
        return str(self.alltime)

@receiver(post_save, sender=Item)
def create_item(sender, instance, created, **kwargs):
    if created:
        Popularity.objects.create(item=instance)

