from django.test import TestCase # used for DB transactions to reset state between tests
from django.core.urlresolvers import reverse

class IndexViewTests(TestCase):
    def test_index_view_with_no_query_params(self):
        """
        If no questions exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('search:index'))
        self.assertTemplateUsed(response, 'search/index.htmldjango')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<input id="searchbar" type="search" placeholder="Search" class="form-control input-lg" />', html=True)

    def test_index_view_with_search_query_params(self):
        """
        If no questions exist, an appropriate message should be displayed.
        """
        context = {'query': 'test search'}
        response = self.client.get(reverse('search:index'), context)
        self.assertTemplateUsed(response, 'search/index.htmldjango')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['search_query'], context['query'])
        self.assertContains(response, '<input id="searchbar" type="search" value="test search" placeholder="Search" class="form-control input-lg" />', html=True)
