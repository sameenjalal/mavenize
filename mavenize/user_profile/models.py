from django.db import models
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.template.defaultfilters import slugify

from social_auth.models import UserSocialAuth
from mavenize.social_graph.models import Following
from mavenize.social_graph.models import Follower

from social_auth.backends.facebook import FacebookBackend
from social_auth.signals import socialauth_registered

from urllib2 import urlopen, HTTPError
import facebook

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    picture_small = models.ImageField(upload_to='img/users',
        default='img/users/default_small.jpg')
    picture_large = models.ImageField(upload_to='img/users',
        default='img/users/default_large.jpg')
    reviews = models.IntegerField(default=0)
    thanks_received = models.BigIntegerField(default=0)
    thanks_given = models.BigIntegerField(default=0)

## Signal handler when a user is created
#def create_user_profile(send, instance, created, **kwargs):
#    if created:
#        profile = UserProfile.objects.create(user=instance)
#        profile.picture_small.save(
#            unicode(user_id)+u'.jpg',
#            picture(graph.request("me/picture")['url']),
#            save=True
#        )
#        profile.picture_large.save(
#            unicode(user_id)+u'_large.jpg',
#            picture(graph.request("me/picture", args={'type': 'large'})['url']),
#            save=True
#        )

# Signal handler when a social user signs up
def new_user_handler(sender, user, response, details, **kwargs):
    user.is_new = True
    user_id = user.id
    social_user = user.social_auth.get(provider='facebook')
    graph = facebook.GraphAPI(social_user.extra_data['access_token'])
    friends = graph.get_connections("me", "friends")['data']
    friend_ids = [friend['id'] for friend in friends]

    # Create the user profile and save users' pictures
    if "id" in response:
        try:
            url = None
            if sender == FacebookBackend:
                url = "http://graph.facebook.com/%s/picture" % response["id"]
            
            if url:
                small_picture = urlopen(url, timeout=5)
                large_picture = urlopen(url+'?type=large', timeout=5)
                profile = UserProfile.objects.create(user=user)
                profile.picture_small.save(
                    slugify(user_id)+u'.jpg',
                    ContentFile(small_picture.read()),
                )
                #profile.picture_large.save(
                #    slugify(user_id)+u'_large.jpg',
                #    ContentFile(large_picture.read()),
                #)
        except HttpError:
            pass

    # Create following and follower relationships
    signed_up = UserSocialAuth.objects.filter(uid__in=friend_ids).values_list(
        'user_id',flat=True)
    for friend in signed_up:
        Following.objects.get_or_create(fb_user=user_id, follow=friend)
        Following.objects.get_or_create(fb_user=friend, follow=user_id)
        Follower.objects.get_or_create(fb_user=user_id, follow=friend)
        Follower.objects.get_or_create(fb_user=friend, follow=user_id)

    return False

socialauth_registered.connect(new_user_handler, sender=None)
