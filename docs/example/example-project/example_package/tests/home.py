from selenium import webdriver
import webdriver_test_tools
from webdriver_test_tools.testcase import *

from example_package import config
from example_package.pages.home import HomePage


class HomePageTestCase(WebDriverTestCase):
    """Really contrived example test case"""

    # URL to go to at the start of each test
    SITE_URL = config.SiteConfig.SITE_URL

    # Test Methods

    def test_page_heading(self):
        """Ensure that the page heading text is correct"""
        page_object = HomePage(self.driver)
        heading_text = page_object.get_heading_text()
        self.assertEqual('Example Domain', heading_text)

    def test_more_information_link(self):
        """Test that the 'More information...' link goes to the correct URL"""
        page_object = HomePage(self.driver)
        expected_url = config.SiteConfig.INFO_URL
        page_object.click_more_information_link()
        self.assertUrlChange(expected_url)

