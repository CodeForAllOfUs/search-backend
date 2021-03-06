import json
from urllib.parse import parse_qs
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.cache import cache_control

from .models import Organization, Project, GitHubOrganizationCache, GitHubProjectCache
from .github import GitHubHeartbeat

gh_heartbeat = GitHubHeartbeat()
gh_heartbeat.start()

def index(request):
    try:
        context = {'search_query': request.GET['query']}
    except:
        context = {}

    return render(request, 'codeforallofus_search/index.htmldjango', context)

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

# @TODO: cache all JSON for at least 15 minutes in production
#        @cache_control(max_age=900)
@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
def github_data_orgs(request):
    try:
        github_paths = set(parse_qs(request.GET.urlencode())['github_paths[]'])
    except:
        return HttpResponseBadRequest()

    cached_paths = [item.toJSON() for item in GitHubOrganizationCache.objects.filter(github_path__in=github_paths)]

    gh_heartbeat.enqueue(Organization, github_paths)

    rate_limit = gh_heartbeat.rate_limit
    rate_limit = {
        'remaining': rate_limit['remaining'],
        'reset_date': rate_limit['reset_date'].isoformat(),
    }

    # only send data for the paths already in the cache since fetching the
    # others using the GitHub API will take too long, because of the rate limit.
    # hopefully they'll be in the cache the next time they're requested.
    return JsonResponse({
        'rate_limit':  rate_limit,
        'github_data': cached_paths,
    })

# @TODO: cache all JSON for at least 15 minutes in production
#        @cache_control(max_age=900)
@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
def github_data_projects(request):
    try:
        github_paths = set(parse_qs(request.GET.urlencode())['github_paths[]'])
    except:
        return HttpResponseBadRequest()

    cached_paths = [item.toJSON() for item in GitHubProjectCache.objects.filter(github_path__in=github_paths)]

    gh_heartbeat.enqueue(Project, github_paths)

    rate_limit = gh_heartbeat.rate_limit
    rate_limit = {
        'remaining': rate_limit['remaining'],
        'reset_date': rate_limit['reset_date'].isoformat(),
    }

    # only send data for the paths already in the cache since fetching the
    # others using the GitHub API will take too long, because of the rate limit.
    # hopefully they'll be in the cache the next time they're requested.
    return JsonResponse({
        'rate_limit':  rate_limit,
        'github_data': cached_paths,
    })
