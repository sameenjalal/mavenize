from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.core.urlresolvers import reverse
from django.db.models import get_model, F, Sum
from django.utils import simplejson
from django.utils.html import escape
from django.utils.timesince import timesince

from activity_feed.models import Activity
from bookmark.models import Bookmark
from notification.models import Notification
from leaderboard.models import KarmaAction
from movie.models import Movie, Genre, Actor, Director
from social_graph.models import Forward, Backward
from user_profile.models import UserProfile, UserStatistics

from sorl.thumbnail import get_thumbnail

MODEL_APP_NAME = {
    'user': 'auth',
    'userstatistics': 'user_profile',
    'review': 'review',
    'agree': 'review',
    'thank': 'review',
    'item': 'item',
    'popularity': 'item',
    'movie': 'movie',
    'activity': 'activity_feed',
    'notification': 'notification'
}

"""
GET METHODS
"""
def get_profile(user_id):
    """
    Returns the user, user profile, and user statistics for the
    specified user.
    """
    return User.objects.select_related('userprofile', 'userstatistics') \
                       .get(pk=user_id)

def get_following(user_id):
    """
    Returns a list of user ids who the specified user is following.
        user_id: primary key of the user (integer)
    """
    return list(Forward.objects.filter(source_id=user_id).values_list(
        'destination_id', flat=True))


def get_followers(user_id):
    """
    Returns a list of user ids who follow the specified user.
        user_id: primary key of the user (integer)
    """
    return list(Backward.objects.filter(destination_id=user_id) \
                                .values_list('source_id', flat=True))


def get_bookmarked_items(user_id):
    """
    Returns a list of item ids of bookmarks for the specified user.
        user_id: primary key of the user (integer)
    """
    return list(Bookmark.objects.filter(user=user_id).values_list(
        'item_id', flat=True))

def get_user_activity(user_ids, page):
    """
    Returns the activities of the users specified in a list of user
    IDs in JSON.
        user_ids: primary keys of users (list of integers)
        page: page number (integer)
    """
    activities = Activity.objects.select_related('sender',
                                                 'sender__userprofile') \
                    .prefetch_related('target_object',
                                      'target_object__user',
                                      'target_object__item',
                                      'target_object__item__movie') \
                    .filter(sender__in=user_ids)

    paginator = Paginator(activities, 20)
    
    try:
        next_page = paginator.page(page).next_page_number()
        paginator.page(next_page)
    except (EmptyPage, InvalidPage):
        next_page = ''

    response = [{
        'object_id': activity.object_id,
        'sender_avatar': get_thumbnail(
            activity.sender.userprofile.avatar, '100x100', crop='center').url,
        'rating': activity.target_object.rating,
        'target_url': reverse('movie-profile',
            args=[activity.target_object.item.movie.url]),
        'target_image': get_thumbnail(
            activity.target_object.item.movie.image, 'x295').url,
        'target_title': activity.target_object.item.movie.title,
        'sender_id': activity.sender_id,
        'sender_url': reverse('user-profile', args=[activity.sender_id]),
        'sender_full_name': activity.sender.get_full_name(),
        'verb': activity.verb,
        'target_user_id': activity.target_object.user_id,
        'target_user_url': reverse('user-profile',
            args=[activity.target_object.user_id]),
        'target_user_full_name': activity.target_object.user \
                                         .get_full_name(),
        'target_user_first_name': activity.target_object.user \
                                          .first_name.lower(),
        'text': escape(activity.target_object.text),
        'time_since': timesince(activity.created_at),
        'next': next_page 
    } for activity in activities]

    return simplejson.dumps(response)
 

def get_beneficiary_leaderboard(user_id, start_time):
    """
    Returns the beneficiary leaderboard for a given user between the
    starting time and now.
    """
    beneficiary_rankings = \
        KarmaAction.objects.filter(created_at__gte=start_time) \
                           .filter(recipient=user_id) \
                           .exclude(giver=user_id) \
                           .values('recipient') \
                           .annotate(total_received=Sum('karma')) \
                           .order_by('-total_received')[:5]
    
    return _match_users_with_karma(beneficiary_rankings)


def get_relative_leaderboard(user_id, start_time):
    """
    Returns the relative leaderboard rankings and start index for a
    given user between starting time and now.
        user_id: primary key of the user (integer)
        start_time: starting time (datetime.datetime)
    """
    us = get_following(user_id) + [user_id]
    leaderboard_rankings = \
        KarmaAction.objects.filter(created_at__gte=start_time) \
                           .filter(giver__in=us) \
                           .values('recipient') \
                           .annotate(total_received=Sum('karma')) \
                           .order_by('-total_received')

    try:
        my_ranking = [i for i, v in enumerate(leaderboard_rankings)
            if v['recipient'] == user_id][0]
    except IndexError:
        my_ranking = 0

    start, end = _compute_relative_leaderboard_indexes(my_ranking,
        len(leaderboard_rankings))
    
    return (_match_users_with_karma(leaderboard_rankings[start:end]),
        start)


def _match_users_with_karma(rankings):
    """
    Returns a list of tuples that maps User objects to karma.
        rankings: list of dictionaries that contains user_ids (integer)
            and karma (integer)
    """
    if not rankings:
        return []

    user = rankings[0].keys()[0]
    karma = rankings[0].keys()[1]
    giver_ids = [r[user] for r in rankings]
    ids_to_users = User.objects.select_related(
        'userprofile').in_bulk(giver_ids)
    return [(ids_to_users[r[user]], r[karma]) for r in rankings]


def _compute_relative_leaderboard_indexes(ranking, size):
    """
    Returns a tuple of the start and end indexes for the relative
    leaderboard.
        ranking: ranking of the user (integer)
        size: the number of users in the leaderboard (integer)
    """
    if ranking == 0 or ranking == 1:
        return (0, 5)
    elif ranking == size or ranking == size-1:
        return (max(0, size-5), size)
    else:
        return (max(0, ranking-2), max(size, ranking+3))


def get_movie_thumbnails(time_period, page, filters):
    """
    Returns a list of movie thumbnails and other relevant information
    based on a time period, page, and a set of filters.
        time_period: 'today', 'week', 'month', or 'alltime' (string)
        page: page for the paginator (integer)
        filters: dictionary that maps fields to parameters (dict)
    """
    movies = Movie.objects.filter(**filters) \
            .order_by('-item__popularity__' + time_period) \
            .values('title', 'url', 'synopsis', 'image', 'theater_date') \
            .distinct()
    paginator = Paginator(movies, 12)

    try:
        next_page = paginator.page(page).next_page_number()
        paginator.page(next_page)
    except (EmptyPage, InvalidPage):
        next_page = ''

    response = [{ 
        'title': escape(movie['title']),
        'url': reverse('movie-profile', args=[movie['url']]),
        'synopsis': escape(movie['synopsis'][:140]),
        'image_url': get_thumbnail(movie['image'], 'x285').url,
        'next': next_page 
    } for movie in paginator.page(page)] 

    return simplejson.dumps(response)


def get_user_boxes(my_id, user_ids, page):
    """
    Returns a list of user details required for following and follower
    boxes.
        my_id: user id of the current user (integer)
        user_ids: list of user ids (integers)
        page: page for the paginator (integer)
    """
    my_following = get_following(my_id)
    profiles = UserProfile.objects.select_related('user') \
                                  .filter(pk__in=user_ids)
    paginator = Paginator(profiles, 20)
    current_page_user_ids = [profile.pk for profile in
        paginator.page(page)]
    are_following = list(set(my_following) & set(current_page_user_ids))

    try:
        next_page = paginator.page(page).next_page_number()
        paginator.page(next_page)
    except (EmptyPage, InvalidPage):
        next_page = ''
    
    response = [{
        'id': profile.pk,
        'full_name': profile.user.get_full_name(),
        'about_me': escape(profile.about_me),
        'image_url': get_thumbnail(profile.avatar, '100x100',
            crop='center').url,
        'url': reverse('user-profile', args=[profile.pk]),
        'is_following': True if profile.pk in are_following else False,
        'next': next_page 
    } for profile in paginator.page(page)]

    return simplejson.dumps(response)


def is_following(source_id, destination_id):
    """
    Returns True if the source id is following the destination id.
        source_id: user id of the source (integer)
        destination_id: user id of the destination (integer)
    """
    return True if Forward.objects.filter(source_id=source_id,
                                          destination_id=destination_id)\
                else False


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
def follow(source_id, destination_id):
    """
    Creates a following relationship between the source id and the
    destination id.
        source_id: user id of the source (integer)
        destination_id: user id of the destination (integer)
    """
    Forward.objects.get_or_create(source_id=source_id,
                                  destination_id=destination_id)
    Backward.objects.get_or_create(destination_id=destination_id,
                                   source_id=source_id)

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
def unfollow(source_id, destination_id):
    """
    Deletes a following relationship between the source id and the
    destination id.
        source_id: user id of the source (integer)
        destination_id: user id of the destination (integer)
    """
    Forward.objects.filter(source_id=source_id,
                           destination_id=destination_id).delete()
    Backward.objects.filter(destination_id=destination_id,
                            source_id=source_id).delete()


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
