from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/organizations$', views.organizations, name='organizations'),
    url(r'^api/projects$', views.projects, name='projects'),
    url(r'^api/github-data/organizations$', views.github_data_orgs, name='github_data_orgs'),
    url(r'^api/github-data/projects$', views.github_data_projects, name='github_data_projects'),
]
