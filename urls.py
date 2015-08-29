from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/organizations$', views.organizations, name='organizations'),
    url(r'^api/projects$', views.projects, name='projects'),
    url(r'^api/github-data$', views.github_data, name='github_data'),
]
