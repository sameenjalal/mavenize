from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.http import Http404

from mavenize.review.models import Review
from mavenize.review.models import Thanks

def thank(request, review_id):
	if request.is_ajax():
		review = get_object_or_404(Review, pk=review_id)
		thank, created = Thanks.objects.get_or_create(
			giver = request.user.id,
			review = review
		)
		if created:
			review.up_votes += 1
			review.save()
		return redirect(request.META.get('HTTP_REFERER', None))
	
	else:
		raise Http404
