import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.keys import Keys

import tests.selenium_tools as selenium_tools
from tests.global_vars import drivers


@selenium_tools.set_class_drivers(drivers, default='ff', conveniences=True)
class TestHomepage(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestHomepage, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(TestHomepage, cls).tearDownClass()

    def setUp(self): pass
    def tearDown(self): pass

    @selenium_tools.method_use_drivers('ff', 'ch')
    def test_search_input_exists(self):
        self.driver.get('%s%s' % (self.live_server_url, '/search/'))

        searchbar = self.d('searchbar')
        self.assertEqual('Search', searchbar.get_attribute('placeholder'))

        searchbar = self.q('input#searchbar')
        self.assertEqual(1, len(searchbar))
        self.assertEqual('Search', searchbar[0].get_attribute('placeholder'))
