def get_rating_field(rating):
    """
    Returns the model field that corresponds to an integer rating.
    """
    rating_choices = ['one', 'two', 'three', 'four']
    return rating_choices[rating-1] + '_star'
