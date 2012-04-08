from apps.user_profile.models import UserStatistics

def get_or_create(user):
    """
    Creates a user statistics object for a given user.
    """
    return UserStatistics.objects.get_or_create(user=user)
