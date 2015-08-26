import json
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.cache import cache_control

from .models import Organization, Project

def index(request):
    context = {}

    if 'query' in request.GET:
        context['search_query'] = request.GET['query']

    return render(request, 'search/index.htmldjango', context)

# in Django 1.9, @never_cache will work reliably
@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
def organizations(request):
    data = json.dumps([org.toJSON() for org in Organization.objects.all()])
    return HttpResponse(data, content_type='application/json')

# in Django 1.9, @never_cache will work reliably
@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
def projects(request):
    data = json.dumps([proj.toJSON() for proj in Project.objects.all()])
    return HttpResponse(data, content_type='application/json')
