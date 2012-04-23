from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import get_model

from review.models import Review, ReviewForm

@login_required
def review(request, title, app, model):
    if request.method == 'POST':
        model_object = get_model(app, model)
        review_item = get_object_or_404(model_object, url=title)
        review = {
            'user': request.session['_auth_user_id'],
            'item': review_item.pk,
            'text': request.POST['text'],
            'rating': int(request.POST['rating']),
            'agrees': 0,
            'thanks': 0
        }
        form = ReviewForm(review)
        if (form.is_valid() and not
                Review.objects.filter(user=review['user'],
                                      item=review['item'])):
            form.save()
    
    return redirect(request.META.get('HTTP_REFERER', None))
