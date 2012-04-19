from haystack.forms import SearchForm

def search(request):
    return {'search': SearchForm()}

def thanks(request):
    if request.user.is_authenticated():
        try:
            profile = request.user.get_profile()
            return {'thanks': profile.thanks_received }
        except:
            return {}
    else:
        return {} 
