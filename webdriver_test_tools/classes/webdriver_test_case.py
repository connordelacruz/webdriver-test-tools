# Test Case Superclass

import unittest
from functools import wraps
from webdriver_test_tools.config import WebDriverConfig
from webdriver_test_tools.common import utils
from webdriver_test_tools import test
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


# Test Case Classes

class WebDriverTestCase(unittest.TestCase):
    """Base class for web driver test cases

    This defines the common setUp() and tearDown() tasks. It does not initialize
    self.driver so will not work on its own. Tests should be written with this as their
    parent class. Browser-specific implementations of test cases will be generated when
    running tests.

    **Instances of this class will have the following variables:**

    :var WebDriverTestCase.driver: Selenium WebDriver object
    :var WebDriverTestCase.WebDriverConfig: WebDriverConfig class

    **Tests that implement this class override the following variables:**

    :var WebDriverTestCase.SITE_URL: Go to this URL during setUp(). Tests that implement
        WebDriverTestCase must set this accordingly.
    :var WebDriverTestCase.SKIP_BROWSERS: (Optional) List of browser names to skip test
        generation for. This can be useful if a test case class requires functionality
        that is not implemented in a certain driver, or if its tests are meant for
        specific browsers. Valid browser names are declared in the Browsers class.
    :var WebDriverTestCase.SKIP_MOBILE: (Optional) By default, tests will be
        generated for all enabled browsers, including mobile. If SKIP_MOBILE is set to
        True, don't generate tests for mobile browsers. This can be helpful if the
        layout changes between desktop and mobile viewports would alter the test
        procedures.

    **Browser-specific implementations of this class need to override the following:**

    :function WebDriverTestCase.driver_init: Function that returns a Selenium WebDriver
        object for the browser
    :var WebDriverTestCase.DRIVER_NAME: Name of the browser. This is mostly used in the
        docstrings of generated test classes to indicate what browser the tests are
        being run in
    :var WebDriverTestCase.SHORT_NAME: Short name for the driver used for command line
        args, skipping, etc. Should be all lowercase with no spaces
    :var WebDriverTestCase.CAPABILITIES: The DesiredCapabilities dictionary for the
        browser. Used for initializing BrowserStack remote driver

    **The following attributes are used for running tests on BrowserStack:**

    :var WebDriverTestCase.ENABLE_BS: (Default = False) If set to True, setUp() will
        initialize a Remote webdriver instead of a local one and run tests on
        BrowserStack
    :var WebDriverTestCase.COMMAND_EXECUTOR: Command executor URL. Test generator
        needs to set this with the configured access key and username

    **The following attributes are used for running tests in a headless browser:**

    :var WebDriverTestCase.ENABLE_HEADLESS: (Default = False) If set to True, browser
        implementations with headless browser support will configure their drivers to
        run tests in a headless browser
    """

    # Instance variables
    driver = None
    WebDriverConfig = WebDriverConfig

    # Test case attributes
    SITE_URL = None
    SKIP_BROWSERS = []
    SKIP_MOBILE = None

    # Browser implementation attributes
    DRIVER_NAME = None
    SHORT_NAME = None

    # BrowserStack attributes
    ENABLE_BS = False
    COMMAND_EXECUTOR = None
    CAPABILITIES = None

    # Headless browser attributes
    ENABLE_HEADLESS = False

    def bs_driver_init(self):
        """Initialize driver for BrowserStack

        :return: webdriver.Remote object with the command_executor and
            desired_capabilities parameters set to self.COMMAND_EXECUTOR and
            self.CAPABILITIES respectively.
        """
        self.CAPABILITIES['name'] = self._testMethodName
        return webdriver.Remote(command_executor=self.COMMAND_EXECUTOR,
                                desired_capabilities=self.CAPABILITIES)

    def driver_init(self):
        """Returns an initialized WebDriver object. Browser test case classes must
        implement this
        """
        pass

    def setUp(self):
        """Initialize driver and call ``self.driver.get(self.SITE_URL)``

        If self.ENABLE_BS is False, self.driver gets the returned results of
        self.DRIVER_INIT(). If self.ENABLE_BS is True, self.driver gets the returned
        results of self._bs_driver_init()
        """
        self.driver = self.bs_driver_init() if self.ENABLE_BS else self.driver_init()
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

    @staticmethod
    def skipMobile():
        """Conditionally skip a test method for mobile browsers

        Usage Example:

        .. code:: python

            @WebDriverTestCase.skipMobile()
            test_method(self):
                ...
        """

        def decorator(test_method):
            @wraps(test_method)
            def wrapper(*args, **kwargs):
                test_case_obj = args[0]
                if issubclass(type(test_case_obj), WebDriverMobileTestCase):
                    test_case_obj.skipTest('Skipping for mobile')
                test_method(*args, **kwargs)

            return wrapper

        return decorator

    @staticmethod
    def mobileOnly():
        """Conditionally skip a test method for non-mobile browsers

        Usage Example:

        .. code:: python

            @WebDriverTestCase.mobileOnly()
            test_method(self):
                ...
        """

        def decorator(test_method):
            @wraps(test_method)
            def wrapper(*args, **kwargs):
                test_case_obj = args[0]
                if not issubclass(type(test_case_obj), WebDriverMobileTestCase):
                    test_case_obj.skipTest('Skipping for non-mobile')
                test_method(*args, **kwargs)

            return wrapper

        return decorator


class WebDriverMobileTestCase(WebDriverTestCase):
    """Base class for mobile web driver test cases

    If a test subclasses WebDriverMobileTestCase instead of WebDriverTestCase, tests
    will only be generated for mobile browsers
    """
    SKIP_MOBILE = False


# Browser Driver Implementations

class FirefoxTestCase(WebDriverTestCase):
    """Implementation of WebDriverTestCase using Firefox webdriver

    `Driver download <https://github.com/mozilla/geckodriver/releases>`__

    This driver supports headless browsing:

        `Headless browser info <https://developer.mozilla.org/en-US/Firefox/Headless_mode>`__
    """
    DRIVER_NAME = 'Firefox'
    SHORT_NAME = DRIVER_NAME.lower()
    CAPABILITIES = DesiredCapabilities.FIREFOX.copy()

    def driver_init(self):
        return self.WebDriverConfig.get_firefox_driver(self.ENABLE_HEADLESS)


class ChromeTestCase(WebDriverTestCase):
    """Implementation of WebDriverTestCase using Chrome webdriver

    `Driver download <https://sites.google.com/a/chromium.org/chromedriver/downloads>`__

    This driver supports headless browsing:

        `Headless browser info <https://developers.google.com/web/updates/2017/04/headless-chrome>`__
    """
    DRIVER_NAME = 'Chrome'
    SHORT_NAME = DRIVER_NAME.lower()
    CAPABILITIES = DesiredCapabilities.CHROME.copy()

    def driver_init(self):
        return self.WebDriverConfig.get_chrome_driver(self.ENABLE_HEADLESS)


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
    CAPABILITIES = DesiredCapabilities.SAFARI.copy()

    def driver_init(self):
        return self.WebDriverConfig.get_safari_driver()


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
    CAPABILITIES = DesiredCapabilities.INTERNETEXPLORER.copy()
    # Set version
    CAPABILITIES['version'] = '11'

    def driver_init(self):
        return self.WebDriverConfig.get_ie_driver()


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
    CAPABILITIES = DesiredCapabilities.EDGE.copy()
    # Set version
    CAPABILITIES['version'] = '16'

    def driver_init(self):
        return self.WebDriverConfig.get_edge_driver()


# Mobile browser emulation

class ChromeMobileTestCase(WebDriverMobileTestCase):
    """Implementation of WebDriverTestCase using Chrome webdriver. Emulates mobile
    device layout.

    `Driver download <https://sites.google.com/a/chromium.org/chromedriver/downloads>`__

    `Mobile emulation info <https://sites.google.com/a/chromium.org/chromedriver/mobile-emulation>`__
    """
    DRIVER_NAME = 'Chrome Mobile [Emulated]'
    SHORT_NAME = 'chrome-mobile'
    CAPABILITIES = DesiredCapabilities.CHROME.copy()
    # Set options for mobile emulation
    CAPABILITIES['chromeOptions'] = {
        'mobileEmulation': WebDriverConfig.CHROME_MOBILE_EMULATION,
    }

    def driver_init(self):
        return self.WebDriverConfig.get_chrome_mobile_driver(self.ENABLE_HEADLESS)


class Browsers(object):
    """Constants for browser short names

    :var Browsers.HEADLESS_COMPATIBLE: List of WebDriverTestCase subclasses that
        support test execution in a headless browser
    """
    FIREFOX = FirefoxTestCase.SHORT_NAME
    CHROME = ChromeTestCase.SHORT_NAME
    SAFARI = SafariTestCase.SHORT_NAME
    IE = IETestCase.SHORT_NAME
    EDGE = EdgeTestCase.SHORT_NAME
    CHROME_MOBILE = ChromeMobileTestCase.SHORT_NAME
    # List of browser classes that support headless browsing
    HEADLESS_COMPATIBLE = [
        FirefoxTestCase,
        ChromeTestCase,
        ChromeMobileTestCase,
    ]

