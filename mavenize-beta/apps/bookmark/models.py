from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import F

from item.models import Item
from user_profile.models import UserStatistics
from bookmark.signals import state_changed

class Bookmark(models.Model):
    user = models.ForeignKey(User)
    item = models.ForeignKey(Item)
    is_public = models.BooleanField(default=True)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s bookmarking Item #%s" % (self.user.get_full_name(),
            self.item.id)

    def save(self, *args, **kwargs):
        # Check to see if the bookmark's active status has been changed
        if (self.id):
            old = Bookmark.objects.get(pk=self.id)
            if not old.is_done == self.is_done:
                state_changed.send(sender=Bookmark, 
                    instance=self, is_done=self.is_done)
        super(Bookmark, self).save(*args, **kwargs)

@receiver(state_changed, sender=Bookmark)
def change_bookmark(sender, instance, is_done, **kwargs):
    """
    Decrement the user and item's active bookmarks by one if the bookmark
    is marked done.
    Increment the user and item's active bookmarks by one if the bookmark
    is marked undone.
    """
    if is_done:
        UserStatistics.objects.filter(
            pk__exact=instance.user_id).update(
                bookmarks_active=F('bookmarks_active')-1)
        instance.item.bookmarks_active = F('bookmarks_active') - 1
    else:
        UserStatistics.objects.filter(
            pk__exact=instance.user_id).update(
                bookmarks_active=F('bookmarks_active')+1)
        instance.item.bookmarks_active = F('bookmarks_active') + 1
    instance.item.save()

@receiver(post_save, sender=Bookmark)
def create_bookmark(sender, instance, created, **kwargs):
    """
    Increment the user and item's bookmarks by one and active bookmarks
    by one if it is active.
    Increment the user's and item's bookmarks by one if the bookmark is
    not active.
    """
    if created:
        if instance.is_done:
            UserStatistics.objects.filter(
                pk__exact=instance.user_id).update(
                    bookmarks=F('bookmarks')+1)
        else:
            UserStatistics.objects.filter(
                pk__exact=instance.user_id).update(
                    bookmarks=F('bookmarks')+1,
                    bookmarks_active=F('bookmarks_active')+1
                )
            instance.item.bookmarks_active = F('bookmarks_active') + 1
        instance.item.bookmarks = F('bookmarks') + 1
        instance.item.save()

@receiver(post_delete, sender=Bookmark)
def delete_bookmark(sender, instance, **kwargs):
    """
    Undo the updates of the bookmark.
    """
    if instance.is_done:
        UserStatistics.objects.filter(
            pk__exact=instance.user_id).update(
                bookmarks=F('bookmarks')-1)
    else:
        UserStatistics.objects.filter(
            pk__exact=instance.user_id).update(
                bookmarks=F('bookmarks')-1,
                bookmarks_active=F('bookmarks_active')-1
            )
        instance.item.bookmarks_active = F('bookmarks_active') - 1
    instance.item.bookmarks = F('bookmarks') - 1
    instance.item.save()

