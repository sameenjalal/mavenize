from django.shortcuts import redirect
from mavenize.general_utilities.models import FeedbackForm
from django.contrib.auth.decorators import login_required

@login_required
def feedback(request):
    if request.method == 'POST':
        feedback = {
            'user': request.user.id,
            'message': request.POST['message']
        }
        form = FeedbackForm(feedback)
        if form.is_valid():
            form.save()

    return redirect(request.META.get('HTTP_REFERER', None))
