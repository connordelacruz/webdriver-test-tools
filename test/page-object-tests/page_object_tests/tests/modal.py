from selenium import webdriver
import webdriver_test_tools
from webdriver_test_tools.testcase import *

from page_object_tests import config
from page_object_tests.pages.modal import ModalPage


class ModalObjectTestCase(WebDriverTestCase):
    """Test ModalObject prototype"""

    # URL to go to at the start of each test
    SITE_URL = config.SiteConfig.SITE_URL + ModalPage.PAGE_FILENAME

    # Test Methods

    def test_modal_object(self):
        """Test is_displayed() and click_close_button()"""
        modal_page = ModalPage(self.driver)
        modal_object = modal_page.click_open_modal_button()
        with self.subTest('Open modal'):
            self.assertTrue(modal_object.is_displayed())
        with self.subTest('Close modal'):
            modal_object.click_close_button()
            self.assertFalse(modal_object.is_displayed())

