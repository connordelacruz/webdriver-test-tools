from selenium import webdriver
import webdriver_test_tools
from webdriver_test_tools.testcase import *

from page_object_tests import config
# TODO: rename to clarify it's using YAML
from page_object_tests.pages.modal import ModalPage
from page_object_tests.pages.no_yaml_modal import NoYAMLModalPage


class ModalObjectTestCase(WebDriverTestCase):
    """Test ModalObject prototype"""

    # URL to go to at the start of each test
    SITE_URL = config.SiteConfig.SITE_URL + ModalPage.PAGE_FILENAME

    # Test Methods

    def test_modal_object_yaml(self):
        """Test is_displayed() and click_close_button() (YAML)"""
        modal_page = ModalPage(self.driver)
        self._test_modal_object(modal_page)

    def test_modal_object_no_yaml(self):
        """Test is_displayed() and click_close_button() (no YAML)"""
        modal_page = NoYAMLModalPage(self.driver)
        self._test_modal_object(modal_page)

    def _test_modal_object(self, modal_page):
        modal_object = modal_page.click_open_modal_button()
        with self.subTest('Open modal'):
            self.assertTrue(modal_object.is_displayed())
        with self.subTest('Close modal'):
            modal_object.click_close_button()
            self.assertFalse(modal_object.is_displayed())

