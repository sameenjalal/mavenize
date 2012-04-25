from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import get_model, F

from activity_feed.models import Activity
from notification.models import Notification
from leaderboard.models import KarmaAction
from user_profile.models import UserStatistics

MODEL_APP_NAME = {
    'user': 'auth',
    'userstatistics': 'user_profile',
    'review': 'review',
    'agree': 'review',
    'thank': 'review',
    'item': 'item',
    'movie': 'movie',
    'activity': 'activity_feed',
    'notification': 'notification'
}

"""
GET METHODS
"""
def filter_then_order_by(model_name, order_criteria, **filters):
    """
    Filters a model with filters and orders the results by
    order_criteria.
        model_name: string of class name
        order_criteria: string of field name
        **filters: dictionary that maps fields to criterion
            Ex.: { 'user__pk': 1 }
    """
    model = get_model(MODEL_APP_NAME[model_name], model_name)
    return model.objects.filter(**filters).order_by(order_criteria)

def filter_excluding_me_then_order_by(model_name, obj_id,
                                      order_criteria, **filters):
    """
    Filters a model with filters, excluding obj_id, and orders the
    results by order_criteria.
        model_name: string of class name
        obj_id: the pk to be excluded
        order_criteria: string of field name
        **filters: dictionary that maps fields to criterion
            Ex.: { 'user__pk': 1 }
    """
    model = get_model(MODEL_APP_NAME[model_name], model_name)
    return model.objects.filter(**filters) \
                        .exclude(pk=obj_id) \
                        .order_by(order_criteria)


def filter_then_count(model_name, **filters):
    """
    Filters a model with filters and returns the object count.
    """
    model = get_model(MODEL_APP_NAME[model_name], model_name)
    return model.objects.filter(**filters).count()

def get_content_type(model_name):
    """
    Returns the ContentType for a model name.
    """
    return ContentType.objects.get(
        app_label=MODEL_APP_NAME[model_name], model=model_name)
        
def get_object(model_name, **filters):
    """
    Filters a model with filters and returns a single object.
    """
    model = get_model(MODEL_APP_NAME[model_name], model_name)
    return model.objects.get(**filters)

"""
CREATE METHODS
"""

def queue_activity(sender_id, verb, model_name, obj_id):
    """
    Adds a review or agree to the activity feed.
        sender_id: review.user_id or agree.user_id
        verb: either "raved about" or "re-raved"
        model_name: string of class name 
        obj_id: object.pk
    """
    model = get_model(MODEL_APP_NAME[model_name], model_name)
    try:
        Activity.objects.create(
            sender=User.objects.get(pk=sender_id),
            verb=verb,
            target_object=model.objects.get(pk=obj_id)
        )
    except ObjectDoesNotExist:
        pass

def queue_notification(sender_id, recipient_id, model_name, obj_id):
    """
    Adds a notification for an agree, thanks, bookmark, or follow.
        sender_id: agree.giver_id, thank.giver_id, bookmark.user_id,
            or backward.source_id
        recipient_id: agree.review.user_id, thank.review.user_id,
            0, or backward.destination_id
        model_name: string of class name
        obj_id: object.pk
    """
    model = get_model(MODEL_APP_NAME[model_name], model_name)
    try:
        Notification.objects.create(
            sender_id=sender_id,
            recipient_id=recipient_id,
            notice_object=model.objects.get(pk=obj_id)
        )
    except ObjectDoesNotExist:
        pass

def add_karma_action(recipient_id, giver_id, karma):
    """
    Adds a karma action for a review, thanks, or agree.
        recipient_id: review.user_id, agree.review.user_id, or
            thank.review.user_id
        giver_id: review.user_id, agree.giver_id, or thank.giver_id
        karma: integer value > 0
    """
    try: 
        KarmaAction.objects.create(
            recipient=User.objects.get(pk=recipient_id),
            giver=User.objects.get(pk=giver_id),
            karma=karma
        )
    except ObjectDoesNotExist:
        pass

"""
UPDATE METHODS
"""

def update_statistics(model_name, obj_id, **fields):
    """
    Updates the statistics for a user, review or item after a
    review, thanks, or agree.
        model_name: string of class name
        obj_id: object.pk
        **fields: dictionary that maps fields to integer values
            Ex.: fields = {'karma': 1}
    """
    model = get_model(MODEL_APP_NAME[model_name], model_name)
    model.objects.filter(pk=obj_id).update(
        **dict([(k, F(k)+fields[k]) for k in fields.keys()]))

"""
DELETE METHODS
"""

def remove_activity(sender_id, verb, model_name, obj_id):
    """
    Removes a review (and all related agrees) or agree from the
    activity feed.
        sender_id: review.user_id or agree.user_id
        verb: either "raved about" or "re-raved"
        model_name: string of class name
        obj_id: object.pk
    """
    Activity.objects.get(
        sender=User.objects.get(pk=sender_id),
        verb=verb,
        content_type=ContentType.objects.get(
            app_label=MODEL_APP_NAME[model_name],
            model=model_name),
        object_id=obj_id
    ).delete()

def remove_notification(sender_id, recipient_id, model_name, obj_id):
    """
    Removes a notification for an agree, thanks, bookmark, or follow.
        sender_id: review.user_id or agree.user_id
        recipient_id: review.user_id or agree.user_id
        verb: either "raved about" or "re-raved"
        model_name: string of class name
        obj_id: object.pk
    """
    Notification.objects.get(
        sender_id=sender_id,
        recipient_id=recipient_id,
        content_type=ContentType.objects.get(
            app_label=MODEL_APP_NAME[model_name],
            model=model_name),
        object_id=obj_id,
    ).delete()

def remove_karma_action(recipient_id, giver_id, karma, time_range):
    """
    Removes a karma action for a review, thanks, or agree.
        recipient_id: review.user_id, agree.review.user_id, or
            thank.review.user_id
        giver_id: review.user_id, agree.giver_id, or thank.giver_id
        karma: integer value > 0
        time_range: tuple of datetime objects - (start, end)
    """
    try:
        KarmaAction.objects.filter(
            recipient=User.objects.get(pk=recipient_id),
            giver=User.objects.get(pk=giver_id),
            karma=karma,
            created_at__range=time_range
        )[0].delete()
    except ObjectDoesNotExist:
        pass

def filter_then_delete(model_name, **filters):
    """
    Filters a model with filters and deletes those objects. 
        model_name: string of class name
        **filters: dictionary that maps fields to criterion
            Ex.: { 'user__pk': 1 }
    """
    model = get_model(MODEL_APP_NAME[model_name], model_name)
    model.objects.filter(**filters).delete()
