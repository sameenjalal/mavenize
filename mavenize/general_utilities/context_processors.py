from haystack.forms import SearchForm

def search(request):
    return {'search': SearchForm()}

def thanks(request):
    if request.user.is_authenticated():
        return {'thanks': request.user.get_profile().thanks_received }
    else:
        return {} 
