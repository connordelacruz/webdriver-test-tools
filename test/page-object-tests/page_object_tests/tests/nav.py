from selenium import webdriver
from selenium.webdriver.common.by import By
import webdriver_test_tools
from webdriver_test_tools.testcase import *

from page_object_tests import config
from page_object_tests.pages.yaml_nav import YAMLNavObject


class NavObjectTestCase(WebDriverTestCase):
    """Test NavObject prototype"""

    # URL to go to at the start of each test
    SITE_URL = config.SiteConfig.SITE_URL + YAMLNavObject.PAGE_FILENAME

    # Test Methods
    # TODO: fixed navs, collapsible navs

    def test_nav_object_yaml(self):
        """Test links for pages and sections, hover and click dropdowns (YAML)"""
        nav_object = YAMLNavObject(self.driver)
        self._test_nav_object(nav_object)

    def _test_nav_object(self, nav_object):
        with self.subTest('Test page link'):
            home_url = nav_object.click_link('home')
            self.assertUrlChange(home_url)
            self.driver.get(self.SITE_URL)
        with self.subTest('Test section link'):
            section_id = nav_object.click_link('section3')
            self.assertInView((By.CSS_SELECTOR, section_id))
        with self.subTest('Test hover menu'):
            menu_object = nav_object.hover_over_link('hover-menu')
            # Test is_visible() method and assert that element is visible for consistency
            self.assertTrue(menu_object.is_visible(), msg='is_visible() returned False')
            self.assertVisible(menu_object.locator, msg='Element located with menu_object.locator is invisible')
        with self.subTest('Test click menu'):
            menu_object = nav_object.click_link('click-menu')
            # Test is_visible() method and assert that element is visible for consistency
            self.assertTrue(menu_object.is_visible(), msg='is_visible() returned False')
            self.assertVisible(menu_object.locator, msg='Element located with menu_object.locator is invisible')

