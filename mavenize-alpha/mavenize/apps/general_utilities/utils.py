from django.db.models.loading import get_model

from apps.review.models import Thanks 

def retrieve_objects(ids, app, model, *fields):
    objects = get_model(app, model).objects.filter(pk__in=ids).values(
        *fields)
    id_objects = dict([(o[fields[0]], o) for o in objects])
    return [id_objects[i] for i in ids]

def aggregate_reviews(user, reviews):
    uids = []
    rids = []
    
    for r in reviews:
        uids.append(r['user'])
        rids.append(r['review_id'])

    users = retrieve_objects(
        uids, 'auth', 'User', 'id', 'first_name')
    thanked_reviews = Thanks.objects.filter(review__in=rids).filter(
        giver=user).values_list('review', flat=True)

    for review, user in zip(reviews, users):
        review.update(user)
        if review['review_id'] in thanked_reviews:
            review['thanked'] = True
        else:
            review['thanked'] = False

    return reviews
