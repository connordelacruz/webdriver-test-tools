import unittest
from functools import wraps

from selenium import webdriver

from webdriver_test_tools.config import WebDriverConfig
from webdriver_test_tools.common import utils
from webdriver_test_tools.webdriver.support import test


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

    def assertEnabled(self, element_locator, msg=None):
        """Fail if element is disabled

        :param element_locator: WebDriver locator tuple in the format (By.<attr>, <locator string>)
        """
        if not self.driver.find_element(*element_locator).is_enabled():
            failure_message = 'Element is disabled'
            msg = self._formatMessage(msg, failure_message)
            raise self.failureException(msg)

    def assertDisabled(self, element_locator, msg=None):
        """Fail if element is enabled

        :param element_locator: WebDriver locator tuple in the format (By.<attr>, <locator string>)
        """
        if self.driver.find_element(*element_locator).is_enabled():
            failure_message = 'Element is enabled'
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


