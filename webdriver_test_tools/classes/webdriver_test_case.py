#!/usr/bin/env python3

# Test Case Superclass

# Imports
# ----------------------------------------------------------------

import unittest
from webdriver_test_tools.config import WebDriverConfig
from webdriver_test_tools import test


# Test Case Classes
# ----------------------------------------------------------------

class WebDriverTestCase(unittest.TestCase):
    """Base class for web driver test cases

    This defines the common setUp() and tearDown() tasks. It does not initialize self.driver so will not work on its own. Tests should be written with this as their parent class and have subclasses for each implementation in order to do multi-browser tests
    """

    # Base URL for these tests. Must be set in test case implementations
    SITE_URL = None
    # WebDriver object. Browser-specific subclasses need to initialize this in setUp() before calling super().setUp()
    driver = None

    def setUp(self):
        self.driver.get(self.SITE_URL)

    def tearDown(self):
        self.driver.quit()

    # Assertion methods
    # --------------------------------

    def _locator_string(self, locator):
        """Shorthand for formating locator tuple as a string for failure output

        :param locator: WebDriver locator tuple in the format (By.<attr>, <locator string>)
        """
        return '("{0}", "{1}")'.format(*locator)


    def assertExists(self, element_locator, msg=None):
        """Fail if element doesn't exist

        :param element_locator: WebDriver locator tuple in the format (By.<attr>, <locator string>)
        """
        if not test.element_exists(self.driver, element_locator):
            failure_message = 'No elements located using ' + self._locator_string(element_locator)
            msg = self._formatMessage(msg, failure_message)
            raise self.failureException(msg)


    def assertNotExists(self, element_locator, msg=None):
        """Fail if element exists

        :param element_locator: WebDriver locator tuple in the format (By.<attr>, <locator string>)
        """
        if test.element_exists(self.driver, element_locator):
            failure_message = 'Elements located using ' + self._locator_string(element_locator)
            msg = self._formatMessage(msg, failure_message)
            raise self.failureException(msg)


    def assertInView(self, element_locator, msg=None):
        """Fail if element isn't scrolled into view

        :param element_locator: WebDriver locator tuple in the format (By.<attr>, <locator string>)
        """
        if not test.in_view_change_test(self.driver, element_locator):
            failure_message = 'Element is not scrolled into view'
            msg = self._formatMessage(msg, failure_message)
            raise self.failureException(msg)


    def assertNotInView(self, element_locator, msg=None):
        """Fail if element is scrolled into view

        :param element_locator: WebDriver locator tuple in the format (By.<attr>, <locator string>)
        """
        if test.in_view_change_test(self.driver, element_locator):
            failure_message = 'Element is scrolled into view'
            msg = self._formatMessage(msg, failure_message)
            raise self.failureException(msg)


    def assertVisible(self, element_locator, msg=None):
        """Fail if element isn't visible

        :param element_locator: WebDriver locator tuple in the format (By.<attr>, <locator string>)
        """
        if not test.visibility_change_test(self.driver, element_locator):
            failure_message = 'Element is not visible'
            msg = self._formatMessage(msg, failure_message)
            raise self.failureException(msg)


    def assertInvisible(self, element_locator, msg=None):
        """Fail if element is visible

        :param element_locator: WebDriver locator tuple in the format (By.<attr>, <locator string>)
        """
        if not test.visibility_change_test(self.driver, element_locator, test_visible=False):
            failure_message = 'Element is visible'
            msg = self._formatMessage(msg, failure_message)
            raise self.failureException(msg)


    def assertUrlChange(self, expected_url, msg=None):
        """Fail if the URL doesn't match the expected URL.

        Assertion uses webdriver_test_tools.test.url_change_test() using the default 10
        second wait timeout before determining that expected_url does not match the
        current URL.

        :param expected_url: The expected URL
        """
        if not test.url_change_test(self.driver, expected_url):
            failure_message = 'Current URL = {}, expected URL = {}'.format(self.driver.current_url, expected_url)
            msg = self._formatMessage(msg, failure_message)
            raise self.failureException(msg)


# Browser driver implementations
# --------------------------------

class FirefoxTestCase(WebDriverTestCase):
    """Implementation of WebDriverTestCase using Firefox webdriver

    `Driver download <https://github.com/mozilla/geckodriver/releases>`__
    """
    DRIVER_NAME = 'Firefox'
    SHORT_NAME = DRIVER_NAME.lower()

    def setUp(self):
        self.driver = WebDriverConfig.get_firefox_driver()
        super().setUp()


class ChromeTestCase(WebDriverTestCase):
    """Implementation of WebDriverTestCase using Chrome webdriver

    `Driver download <https://sites.google.com/a/chromium.org/chromedriver/downloads>`__
    """
    DRIVER_NAME = 'Chrome'
    SHORT_NAME = DRIVER_NAME.lower()

    def setUp(self):
        self.driver = WebDriverConfig.get_chrome_driver()
        super().setUp()


# Experimental/Platform-specific

class SafariTestCase(WebDriverTestCase):
    """Implementation of WebDriverTestCase using Safari webdriver

    `Driver info <https://webkit.org/blog/6900/webdriver-support-in-safari-10/>`__

    .. warning::

        This class is experimental and has not been fully tested. It is disabled by
        default but can be enabled in ``<test_package>/config/browser.py`` by
        uncommenting the corresponding line in ``BrowserConfig.BROWSER_TEST_CLASSES``.

    .. warning::

        Safari's webdriver can be unreliable and buggy. Apart from starting up a new
        Safari instance each time it's initialized and leaving the process running even
        when driver.quit() is called, it also seems to lack certain features of the
        webdriver API, leading to several inaccurate test failures.
    """
    DRIVER_NAME = 'Safari'
    SHORT_NAME = DRIVER_NAME.lower()

    def setUp(self):
        self.driver = WebDriverConfig.get_safari_driver()
        super().setUp()


class IETestCase(WebDriverTestCase):
    """Implementation of WebDriverTestCase using Internet Explorer webdriver

    `Driver info <https://github.com/SeleniumHQ/selenium/wiki/InternetExplorerDriver>`__

    .. warning::

        This class is experimental and has not been fully tested. It is disabled by
        default but can be enabled in ``<test_package>/config/browser.py`` by
        uncommenting the corresponding line in ``BrowserConfig.BROWSER_TEST_CLASSES``.
    """
    DRIVER_NAME = 'Internet Explorer'
    SHORT_NAME = 'ie'

    def setUp(self):
        self.driver = WebDriverConfig.get_ie_driver()
        super().setUp()


class EdgeTestCase(WebDriverTestCase):
    """Implementation of WebDriverTestCase using Edge webdriver

    `Driver download <https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/>`_

    .. warning::

        This class is experimental and has not been fully tested. It is disabled by
        default but can be enabled in ``<test_package>/config/browser.py`` by
        uncommenting the corresponding line in ``BrowserConfig.BROWSER_TEST_CLASSES``.
    """
    DRIVER_NAME = 'Edge'
    SHORT_NAME = DRIVER_NAME.lower()

    def setUp(self):
        self.driver = WebDriverConfig.get_edge_driver()
        super().setUp()

