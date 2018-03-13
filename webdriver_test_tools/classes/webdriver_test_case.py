#!/usr/bin/env python3

# Test Case Superclass

# Imports
# ----------------------------------------------------------------

import unittest
from webdriver_test_tools.config import WebDriverConfig


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


# Browser driver implementations
# --------------------------------

class FirefoxTestCase(WebDriverTestCase):
    """Implementation of WebDriverTestCase using Firefox webdriver

    `Driver download <https://github.com/mozilla/geckodriver/releases>`_
    """
    DRIVER_NAME = 'Firefox'
    SHORT_NAME = DRIVER_NAME.lower()

    def setUp(self):
        self.driver = WebDriverConfig.get_firefox_driver()
        super().setUp()


class ChromeTestCase(WebDriverTestCase):
    """Implementation of WebDriverTestCase using Chrome webdriver

    `Driver download <https://sites.google.com/a/chromium.org/chromedriver/downloads>`_
    """
    DRIVER_NAME = 'Chrome'
    SHORT_NAME = DRIVER_NAME.lower()

    def setUp(self):
        self.driver = WebDriverConfig.get_chrome_driver()
        super().setUp()


# Experimental/Platform-specific

class SafariTestCase(WebDriverTestCase):
    """Implementation of WebDriverTestCase using Safari webdriver

    `Driver info <https://webkit.org/blog/6900/webdriver-support-in-safari-10/>`_

    .. warning::

        Safari's webdriver can be unreliable and buggy. Apart from starting up a new
        Safari instance each time it's initialized and leaving the process running even
        when driver.quit() is called, it also seems to lack certain features of the
        webdriver API, leading to several inaccurate test failures. As such, the class
        currently isn't implemented. It may be enabled in a future update.
    """
    DRIVER_NAME = 'Safari'
    SHORT_NAME = DRIVER_NAME.lower()

    def setUp(self):
        self.driver = WebDriverConfig.get_safari_driver()
        super().setUp()


class IETestCase(WebDriverTestCase):
    """Implementation of WebDriverTestCase using Internet Explorer webdriver

    .. warning::

        This class has not been tested yet and isn't implemented. It may be enabled in
        a future update.
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

        This class has not been tested yet and isn't implemented. It may be enabled in
        a future update.
    """
    DRIVER_NAME = 'Edge'
    SHORT_NAME = DRIVER_NAME.lower()

    def setUp(self):
        self.driver = WebDriverConfig.get_edge_driver()
        super().setUp()


# Dictionary of usable test case classes indexed by the short name for that class (i.e. its command line argument)
BROWSER_TEST_CLASSES = {
    FirefoxTestCase.SHORT_NAME: FirefoxTestCase,
    ChromeTestCase.SHORT_NAME: ChromeTestCase,
    # SafariTestCase.SHORT_NAME: SafariTestCase,
    # IETestCase.SHORT_NAME: IETestCase,
    # EdgeTestCase.SHORT_NAME: EdgeTestCase,
}


