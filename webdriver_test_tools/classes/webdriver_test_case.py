# Test Case Superclass

import unittest
from functools import wraps
from webdriver_test_tools.config import WebDriverConfig
from webdriver_test_tools.common import utils
from webdriver_test_tools import test


# Test Case Classes

class WebDriverTestCase(unittest.TestCase):
    """Base class for web driver test cases

    This defines the common setUp() and tearDown() tasks. It does not initialize
    self.driver so will not work on its own. Tests should be written with this as their
    parent class. Browser-specific implementations of test cases will be generated when
    running tests

    **Tests that implement this class override the following variables:**

    :var WebDriverTestCase.SITE_URL: Go to this URL during setUp(). Tests that implement
        WebDriverTestCase must set this accordingly.
    :var WebDriverTestCase.SKIP_BROWSERS: (Optional) List of browser names to skip test
        generation for. This can be useful if a test case class requires functionality
        that is not implemented in a certain driver, or if its tests are meant for
        specific browsers. Valid browser names are declared in the Browsers class.

    **Browser-specific implementations of this class need to override the following:**

    :var WebDriverTestCase.driver: Selenium WebDriver object. Need to initialize this
        in setUp() before calling super().setUp()
    :var WebDriverTestCase.DRIVER_NAME: Name of the browser. This is mostly used in the
        docstrings of generated test classes to indicate what browser the tests are
        being run in
    :var WebDriverTestCase.SHORT_NAME: Short name for the driver used for command line
        args, skipping, etc. Should be all lowercase with no spaces
    """

    # Test case attributes
    SITE_URL = None
    SKIP_BROWSERS = []

    # Browser implementation attributes
    driver = None
    DRIVER_NAME = None
    SHORT_NAME = None

    def setUp(self):
        """Calls ``self.driver.get(self.SITE_URL)``"""
        self.driver.get(self.SITE_URL)

    def tearDown(self):
        """Calls ``self.driver.quit()``"""
        self.driver.quit()

    # Assertion methods

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

    def assertBaseUrlChange(self, expected_url, msg=None):
        """Fail if the URL (ignoring query strings) doesn't match the expected URL.

        Assertion uses webdriver_test_tools.test.url_change_test() using the default 10
        second wait timeout before determining that expected_url does not match the
        current URL.

        :param expected_url: The expected URL
        """
        if not test.base_url_change_test(self.driver, expected_url):
            failure_message = 'Current base URL = {}, expected base URL = {}'.format(
                utils.get_base_url(self.driver.current_url), expected_url)
            msg = self._formatMessage(msg, failure_message)
            raise self.failureException(msg)

    # Skipping Browsers
    @staticmethod
    def skipBrowsers(*browsers):
        """Conditionally skip a test method for certain browsers

        Usage Example:

        .. code:: python

            @WebDriverTestCase.skipBrowsers(Browsers.SAFARI, Browsers.IE)
            test_method(self):
                ...
        """
        def decorator(test_method):
            @wraps(test_method)
            def wrapper(*args, **kwargs):
                test_case_obj = args[0]
                if test_case_obj.SHORT_NAME in browsers:
                    test_case_obj.skipTest('Skipping {}'.format(test_case_obj.DRIVER_NAME))
                test_method(*args, **kwargs)
            return wrapper
        return decorator

# Browser Driver Implementations

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

        Safari's webdriver is missing certain features of the webdriver API, which can
        cause test failures. As of Safari 11.0.3, issues with the following modules
        have been encountered during testing:

            - ``selenium.webdriver.common.action_chains``
            - ``selenium.webdriver.support.select``
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


class Browsers(object):
    """Constants for browser short names"""
    FIREFOX = FirefoxTestCase.SHORT_NAME
    CHROME = ChromeTestCase.SHORT_NAME
    SAFARI = SafariTestCase.SHORT_NAME
    IE = IETestCase.SHORT_NAME
    EDGE = EdgeTestCase.SHORT_NAME


