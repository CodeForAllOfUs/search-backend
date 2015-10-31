import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.keys import Keys

import tests.selenium_tools as selenium_tools
from tests.global_vars import drivers


class TestHomepage(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestHomepage, cls).setUpClass()
        cls.drivers = drivers
        cls.driver  = drivers.get('ff')

    @classmethod
    def tearDownClass(cls):
        super(TestHomepage, cls).tearDownClass()

    def setUp(self): pass
    def tearDown(self): pass

    @selenium_tools.use_drivers('ff', 'ch')
    def test_search_input_exists(self):
        d = self.driver.find_elements_by_css_selector
        self.driver.get('%s%s' % (self.live_server_url, '/search/'))

        searchbar = d('input#searchbar')
        self.assertEqual(1, len(searchbar))
        self.assertEqual('Search', searchbar[0].get_attribute('placeholder'))
