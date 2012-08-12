from django.template import loader, Context
from django.http import HttpResponse

def a(request):
    t = loader.get_template('a.html')
    c = Context({})
    return HttpResponse(t.render(c))
	
