from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import receiver

from social_auth.signals import pre_update
from social_auth.backends.facebook import FacebookBackend
from social_auth.models import UserSocialAuth
import facebook

class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    avatar = models.ImageField(
        upload_to='img/users/avatars',
        default='img/users/avatars/default.jpg',
    )
    thumbnail = models.ImageField(
        upload_to='img/users',
        default='img/users/thumbnails/default.jpg',
    )
    gender = models.CharField(max_length=1)

    def __unicode__(self):
        return self.user.get_full_name()

class UserStatistics(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    karma = models.IntegerField(default=0)
    reviews = models.IntegerField(default=0)
    bookmarks = models.IntegerField(default=0)
    bookmarks_active = models.IntegerField(default=0)
    agrees_out = models.IntegerField(default=0)
    agrees_in = models.IntegerField(default=0)
    thanks_out = models.IntegerField(default=0)
    thanks_in = models.IntegerField(default=0)

    def __unicode__(self):
        return "%s: %s" % (self.user.get_full_name(), self.karma)

class KarmaUser(User):
    class Meta:
        proxy = True

    def get_statistics(self):
        """
        Returns the UserStatistics model for this user.
        """
        if not hasattr(self, '_statistics_cache'):
            try:
                self._statistics_cache = UserStatistics.objects.get( 
                    user__id__exact=self.id)
                self._statistics_cache.user = self
            except:
                raise ObjectDoesNotExist 
        return self._statistics_cache

@receiver(pre_update, sender=FacebookBackend)
def update_user_profile(sender, user, response, details, **kwargs):
    profile, created = UserProfile.objects.get_or_create(user=user)
    statistics, created = UserStatistics.objects.get_or_create(
        user=user)

    if "id" in response:
        from urllib2 import urlopen, HTTPError
        from django.template.defaultfilters import slugify
        from django.core.files.base import ContentFile

        try:
            url = "http://graph.facebook.com/%s/picture" \
                % response["id"]
            avatar = urlopen(url+'?type=large', timeout=15)
            thumbnail = urlopen(url, timeout=15)
            profile.avatar.save(slugify(user.id + 'a') + u'.jpg',
                ContentFile(avatar.read()))
            profile.thumbnail.save(slugify(user.id + 't') + u'.jpg',
                ContentFile(thumbnail.read()))
        except HTTPError:
            pass
    
    return True

#@receiver(post_save, sender=User)
#def create_user(sender, instance, created, **kwargs):
#    """
#    Create a user profile and user statistics for this user.
#    """
#    if created:
#        UserProfile.objects.create(user=instance)
#        UserStatistics.objects.create(user=instance)
#
#@receiver(post_save, sender=KarmaUser)
#def create_karma_user(sender, instance, created, **kwargs):
#    """
#    Create a user profile and user statistics for this user.
#    """
#    if created:
#        UserProfile.objects.create(user=instance)
#        UserStatistics.objects.create(user=instance)
