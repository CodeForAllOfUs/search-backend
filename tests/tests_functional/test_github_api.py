import datetime

from django.test import TestCase # used for DB transactions to reset state between tests
from django.core.urlresolvers import reverse

from codeforallofus_search.models import Tag

# Create your tests here.

# ref: https://docs.djangoproject.com/en/1.8/topics/testing/tools/#django.test.LiveServerTestCase

class IndexViewTests(TestCase):
    def test_index_view_with_no_query_params(self):
        response = self.client.get(reverse('codeforallofus_search:index'))
        self.assertTemplateUsed(response, 'codeforallofus_search/index.htmldjango')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<input id="searchbar" type="search" placeholder="Search" class="form-control input-lg" />', html=True)

    def test_index_view_with_search_query_param(self):
        context = {'query': 'test search'}
        response = self.client.get(reverse('codeforallofus_search:index'), context)
        self.assertTemplateUsed(response, 'codeforallofus_search/index.htmldjango')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['search_query'], context['query'])
        self.assertContains(response, '<input id="searchbar" type="search" value="{}" placeholder="Search" class="form-control input-lg" />'.format(context['query']), html=True)
