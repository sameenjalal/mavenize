from django.contrib.auth.models import User
from django.db.models import F
from celery.task import celery

from activity_feed.models import Activity
from notification.models import Notification
from leaderboard.models import KarmaAction
from user_profile.models import UserStatistics

@task(ignore_result=True)
def queue_activity(sender_id, verb, obj_model, obj_id):
    """
    Adds a review or agree to the activity feed.
        sender_id: review.user_id or agree.user_id
        verb: either "raved about" or "re-raved"
        object_model: object.__class__
        object_id: object.pk
    """
    Activity.objects.create(
        sender=User.objects.get(pk=sender_id),
        verb=verb,
        target_object=obj_model.objects.get(pk=obj_id)
    )

@task(ignore_result=True)
def queue_notification(sender_id, recipient_id, obj_model, obj_id):
    """
    Adds a notification for an  agree, thanks, bookmark, or follow.
        sender_id: agree.giver_id, thank.giver_id, bookmark.user_id,
            or backward.source_id
        recipient_id: agree.review.user_id, thank.review.user_id,
            0, or backward.destination_id
        obj_model: object.__class__
        obj_id: object.pk
    """
    Notification.objects.create(
        sender_id=sender_id,
        recipient_id=recipient_id,
        notice_object=obj_model.objects.get(pk=obj_id)
    )

@task(ignore_result=True)
def add_karma_action(recipient_id, giver_id, karma):
    """
    Adds a karma action for a review, thanks, or agree.
        recipient_id: review.user_id, agree.review.user_id, or
            thank.review.user_id
        giver_id: review.user_id, agree.giver_id, or thank.giver_id
        karma: integer value > 0
    """
    KarmaAction.objects.create(
        recipient=User.objects.get(pk=recipient_id),
        giver=User.objects.get(pk=giver_id),
        karma=karma
    )

@task(ignore_result=True)
def update_statistics(obj_model, obj_id, **fields):
    """
    Updates the statistics for a user, review or item after a
    review, thanks, or agree.
        **fields: dictionary that maps fields to integer values
            Ex.: fields = {'karma': 1}
    """
    obj_model.objects.filter(pk=obj_id).update(
        **dict([(k, F(k)+fields[k]) for k in fields.keys()]))

