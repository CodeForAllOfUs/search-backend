import json
from django.shortcuts import render
from django.http import HttpResponse

from .models import Organization, Project

def index(request):
    context = {}

    if 'query' in request.GET:
        context['search_query'] = request.GET['query']

    return render(request, 'search/index.htmldjango', context)

def organizations(request):
    data = json.dumps([org.toJSON() for org in Organization.objects.all()])
    return HttpResponse(data, content_type='application/json')

def projects(request):
    data = json.dumps([proj.toJSON() for proj in Project.objects.all()])
    return HttpResponse(data, content_type='application/json')
