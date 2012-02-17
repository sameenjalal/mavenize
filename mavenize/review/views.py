from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.http import Http404

from mavenize.review.models import Review
from mavenize.review.models import Thanks

from django.contrib.auth.decorators import login_required

@login_required
def thank(request, review_id):
    if request.is_ajax():
        review = get_object_or_404(Review, pk=review_id)
        thank, created = Thanks.objects.get_or_create(
            giver = request.user.id,
            review = review
        )
        if created:
            receiver_profile = review.user.get_profile()
            giver_profile = request.user.get_profile()

            review.up_votes += 1
            review.save()
            receiver_profile.thanks_received += 1
            receiver_profile.save()
            giver_profile.thanks_given += 1
            giver_profile.save()

        return redirect(request.META.get('HTTP_REFERER', None))
    
    else:
        raise Http404
