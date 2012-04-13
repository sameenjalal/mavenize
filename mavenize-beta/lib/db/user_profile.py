from apps.user_profile.models import UserProfile

def get_or_create(user):
    """
    Creates a user profile object for a given user.
    """
    return UserProfile.objects.get_or_create(user=user)

