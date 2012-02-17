from haystack.forms import SearchForm

def search(request):
    return {'search': SearchForm()}
