from django.db import models
from django.dispatch import receiver

from social_auth.signals import pre_update
from social_auth.backends.facebook import FacebookBackend
from social_auth.models import UserSocialAuth
import facebook

class Forward(models.Model):
    source_id = models.BigIntegerField(db_index=True)
    destination_id = models.BigIntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "User #%s following User #%s" % (self.source_id,
            self.destination_id)

class Backward(models.Model):
    destination_id = models.BigIntegerField(db_index=True)
    source_id = models.BigIntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "User #%s following User #%s" % (self.source_id,
            self.destination_id)

@receiver(pre_update, sender=FacebookBackend)
def build_social_graph(sender, user, response, details, **kwargs):
    """
    Update user social graph using Facebook friends.
    """
    social_user = user.social_auth.get(provider='facebook')
    graph = facebook.GraphAPI(social_user.extra_data['access_token'])
    friends = graph.get_connections("me", "friends")['data']
    friend_ids = [friend['id'] for friend in friends]
    signed_up = UserSocialAuth.objects.filter(
        uid__in=friend_ids).values_list('user_id', flat=True)
    already_following = Forward.objects.filter(
        source_id=user.id).values_list('destination_id', flat=True)
    to_add = list(set(signed_up) - set(already_following))

    forward_rel = [Forward(source_id=user.id, destination_id=fid)
            for fid in to_add]
    forward_rel += ([Forward(source_id=fid, destination_id=user.id)
            for fid in to_add])
    backward_rel = [Backward(destination_id=fid, source_id=user.id)
            for fid in to_add]
    backward_rel += ([Backward(destination_id=user.id, source_id=fid)
            for fid in to_add])
    Forward.objects.bulk_create(forward_rel)
    Backward.objects.bulk_create(backward_rel)
