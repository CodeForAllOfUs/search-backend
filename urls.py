from django.conf.urls import include, url
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^data/organizations.json$', RedirectView.as_view(url='/static/search/data/organizations.json', permanent=False)),
    url(r'^data/projects.json$', RedirectView.as_view(url='/static/search/data/projects.json', permanent=False)),
]
