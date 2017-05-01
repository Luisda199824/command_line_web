from django.http import HttpResponse
from django.template import loader

def index(request):
    template = loader.get_template('index.html')
    ctx = {}
    return HttpResponse(template.render(ctx, request))
