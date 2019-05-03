from selenium import webdriver
import webdriver_test_tools
from webdriver_test_tools.testcase import *

from page_object_tests import config
from page_object_tests.pages.web_page import (
    YAMLWebPageRelative, YAMLWebPageFullURL, NoYAMLWebPage
)


class WebPageObjectTestCase(WebDriverTestCase):
    """Test WebPageObject prototype"""

    # URL to go to at the start of each test
    SITE_URL = NoYAMLWebPage.PAGE_URL

    # Test Methods

    def test_web_page_object_no_yaml(self):
        """Test PAGE_URL (no YAML)"""
        web_page_object = NoYAMLWebPage(self.driver)
        self.assertUrlChange(web_page_object.PAGE_URL)

    def test_web_page_object_yaml(self):
        """Test PAGE_URL (YAML)"""
        with self.subTest('WebPageObject with path/relative_to in YAML'):
            web_page_object = YAMLWebPageRelative(self.driver)
            self.driver.get(web_page_object.PAGE_URL)
            self.assertUrlChange(web_page_object.PAGE_URL)
        with self.subTest('WebPageObject with full URL string in YAML'):
            web_page_object = YAMLWebPageFullURL(self.driver)
            self.driver.get(web_page_object.PAGE_URL)
            self.assertUrlChange(web_page_object.PAGE_URL)

