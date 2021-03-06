from selenium import webdriver
from selenium.webdriver.common.by import By
import webdriver_test_tools
from webdriver_test_tools.testcase import *

from page_object_tests import config
from page_object_tests.pages.nav import (
    YAMLNav, YAMLNavFixed,
    YAMLCollapsibleNav, YAMLNavCollapsibleSubclass, YAMLCollapsibleNavFixed,
    NoYAMLNav, NoYAMLNavFixed,
    NoYAMLCollapsibleNav, NoYAMLCollapsibleNavFixed
)


class NavObjectTestCase(WebDriverTestCase):
    """Test NavObject prototype (COLLAPSIBLE = False, FIXED = False)"""

    # URL to go to at the start of each test
    SITE_URL = config.SiteConfig.SITE_URL + YAMLNav.PAGE_FILENAME

    # Test Methods

    def test_nav_object_yaml(self):
        """(Non-collapsible) Test links for pages and sections, hover and click dropdowns (YAML)"""
        nav_object = YAMLNav(self.driver)
        self._test_nav_object(nav_object)

    def test_nav_object_no_yaml(self):
        """(Non-collapsible) Test links for pages and sections, hover and click dropdowns (no YAML)"""
        nav_object = NoYAMLNav(self.driver)
        self._test_nav_object(nav_object)

    # TODO: extract to superclass?
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


class FixedNavObjectTestCase(WebDriverTestCase):
    """Test NavObject prototype (COLLAPSIBLE = False, FIXED = True)"""

    # URL to go to at the start of each test
    SITE_URL = config.SiteConfig.SITE_URL + YAMLNavFixed.PAGE_FILENAME

    # Test Methods

    def test_fixed_nav_object_yaml(self):
        """(Non-collapsible, fixed) Test links for pages and sections, hover and click dropdowns (YAML)"""
        nav_object = YAMLNavFixed(self.driver)
        self._test_nav_object(nav_object)

    def test_fixed_nav_object_no_yaml(self):
        """(Non-collapsible, fixed) Test links for pages and sections, hover and click dropdowns (no YAML)"""
        nav_object = NoYAMLNavFixed(self.driver)
        self._test_nav_object(nav_object)

    # TODO: extract to superclass?
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


class CollapsibleNavObjectTestCase(WebDriverTestCase):
    """Test NavObject prototype (COLLAPSIBLE = True, FIXED = False)"""

    # URL to go to at the start of each test
    SITE_URL = config.SiteConfig.SITE_URL + YAMLCollapsibleNav.PAGE_FILENAME

    # Test Methods

    def test_nav_object_yaml(self):
        """(Collapsible) Test links for pages and sections and click dropdowns (YAML)"""
        nav_object = YAMLCollapsibleNav(self.driver)
        self._test_nav_object(nav_object)

    def test_nav_object_no_yaml(self):
        """(Collapsible) Test links for pages and sections and click dropdowns (no YAML)"""
        nav_object = NoYAMLCollapsibleNav(self.driver)
        self._test_nav_object(nav_object)

    def test_nav_object_collapsible_subclass(self):
        """(Collapsible) Test links for pages and sections and click dropdowns (subclass of YAML)"""
        nav_object = YAMLNavCollapsibleSubclass(self.driver)
        self._test_nav_object(nav_object)

    def _test_nav_object(self, nav_object):
        with self.subTest('Expand nav menu'):
            nav_object.click_expand_button()
            # Test is_expanded() method and assert that element is visible for consistency
            # TODO: animation causes false positive, so is_expanded() not properly tested
            # self.assertTrue(nav_object.is_expanded(), msg='is_expanded() returned False')
            self.assertVisible(nav_object.MENU_LOCATOR, msg='Element located with nav_object.MENU_LOCATOR is invisible')
        with self.subTest('Collapse nav menu'):
            nav_object.click_collapse_button()
            # Test is_expanded() method and assert that element is not visible for consistency
            # TODO: animation causes false positive, so is_expanded() not properly tested
            # self.assertFalse(nav_object.is_expanded(), msg='is_expanded() returned True')
            self.assertInvisible(nav_object.MENU_LOCATOR, msg='Element located with nav_object.MENU_LOCATOR is visible')
        with self.subTest('Test page link'):
            home_url = nav_object.click_link('home')
            self.assertUrlChange(home_url)
            self.driver.get(self.SITE_URL)
        with self.subTest('Test section link'):
            if not nav_object.is_expanded():
                nav_object.click_expand_button()
            section_id = nav_object.click_link('section3')
            self.assertInView((By.CSS_SELECTOR, section_id))
        with self.subTest('Test click menu'):
            if not nav_object.is_expanded():
                nav_object.click_expand_button()
            menu_object = nav_object.click_link('click-menu')
            # Test is_visible() method and assert that element is visible for consistency
            self.assertTrue(menu_object.is_visible(), msg='is_visible() returned False')
            self.assertVisible(menu_object.locator, msg='Element located with menu_object.locator is invisible')


class FixedCollapsibleNavObjectTestCase(WebDriverTestCase):
    """Test NavObject prototype (COLLAPSIBLE = True, FIXED = True)"""

    # URL to go to at the start of each test
    SITE_URL = config.SiteConfig.SITE_URL + YAMLCollapsibleNavFixed.PAGE_FILENAME

    # Test Methods

    def test_nav_object_yaml(self):
        """(Collapsible, fixed) Test links for pages and sections and click dropdowns (YAML)"""
        nav_object = YAMLCollapsibleNavFixed(self.driver)
        self._test_nav_object(nav_object)

    def test_nav_object_no_yaml(self):
        """(Collapsible, fixed) Test links for pages and sections and click dropdowns (no YAML)"""
        nav_object = NoYAMLCollapsibleNavFixed(self.driver)
        self._test_nav_object(nav_object)

    def _test_nav_object(self, nav_object):
        with self.subTest('Expand nav menu'):
            nav_object.click_expand_button()
            # Test is_expanded() method and assert that element is visible for consistency
            # TODO: animation causes false positive, so is_expanded() not properly tested
            # self.assertTrue(nav_object.is_expanded(), msg='is_expanded() returned False')
            self.assertVisible(nav_object.MENU_LOCATOR, msg='Element located with nav_object.MENU_LOCATOR is invisible')
        with self.subTest('Collapse nav menu'):
            nav_object.click_collapse_button()
            # Test is_expanded() method and assert that element is not visible for consistency
            # TODO: animation causes false positive, so is_expanded() not properly tested
            # self.assertFalse(nav_object.is_expanded(), msg='is_expanded() returned True')
            self.assertInvisible(nav_object.MENU_LOCATOR, msg='Element located with nav_object.MENU_LOCATOR is visible')
        with self.subTest('Test page link'):
            home_url = nav_object.click_link('home')
            self.assertUrlChange(home_url)
            self.driver.get(self.SITE_URL)
        with self.subTest('Test section link'):
            if not nav_object.is_expanded():
                nav_object.click_expand_button()
            section_id = nav_object.click_link('section3')
            self.assertInView((By.CSS_SELECTOR, section_id))
        with self.subTest('Test click menu'):
            if not nav_object.is_expanded():
                nav_object.click_expand_button()
            menu_object = nav_object.click_link('click-menu')
            # Test is_visible() method and assert that element is visible for consistency
            self.assertTrue(menu_object.is_visible(), msg='is_visible() returned False')
            self.assertVisible(menu_object.locator, msg='Element located with menu_object.locator is invisible')

