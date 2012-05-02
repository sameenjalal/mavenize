import datetime

def get_rating_field(rating):
    """
    Returns the model field that corresponds to an integer rating.
    """
    rating_choices = ['one', 'two', 'three', 'four']
    return rating_choices[rating-1] + '_star'

def decrement_popularities(timestamp, rating):
    """
    Calculates which popularities to decrement based on the timestamp
    of the object being deleted.
    """
    popularity = { 'today': -rating, 'week': -rating, 'month': -rating,
        'alltime': -rating }
    now = datetime.datetime.now()
    if timestamp < now - datetime.timedelta(days=1):
        popularity['today'] = 0
    if timestamp < now - datetime.timedelta(days=7):
        popularity['week'] = 0
    if timestamp < now - datetime.timedelta(days=30):
        popularity['month'] = 0
    return popularity
        

def pop_empty_keys(dictionary):
    """
    Pops the empty keys of a dictiionary.
    """
    for key in dictionary.keys():
        if not dictionary[key] or dictionary[key] == ['']:
            dictionary.pop(key)
    return dictionary
