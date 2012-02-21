from haystack.forms import SearchForm

def search(request):
    return {'search': SearchForm()}

def thanks(request):
    return {'thanks': request.user.get_profile().thanks_received }
