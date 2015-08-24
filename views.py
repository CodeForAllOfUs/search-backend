import json
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context = {}

    if 'query' in request.GET:
        context['search_query'] = request.GET['query']

    return render(request, 'search/index.htmldjango', context)
