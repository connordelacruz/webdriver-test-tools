"""Browser implementations of :class:`WebDriverTestCase
<webdriver_test_tools.testcase.webdriver.WebDriverTestCase>`.

This module imports the following classes:

    :class:`webdriver_test_tools.testcase.chrome.ChromeTestCase`
    :class:`webdriver_test_tools.testcase.chrome.ChromeMobileTestCase`
    :class:`webdriver_test_tools.testcase.firefox.FirefoxTestCase`
    :class:`webdriver_test_tools.testcase.edge.EdgeTestCase`
    :class:`webdriver_test_tools.testcase.ie.IETestCase`
    :class:`webdriver_test_tools.testcase.safari.SafariTestCase`

"""

from .chrome import *
from .edge import *
from .firefox import *
from .ie import *
from .safari import *

class Browsers:
    """Constants for browser short names"""
    FIREFOX = FirefoxTestCase.SHORT_NAME
    CHROME = ChromeTestCase.SHORT_NAME
    SAFARI = SafariTestCase.SHORT_NAME
    IE = IETestCase.SHORT_NAME
    EDGE = EdgeTestCase.SHORT_NAME
    CHROME_MOBILE = ChromeMobileTestCase.SHORT_NAME
    #: Dictionary mapping browser names to their corresponding test classes
    TEST_CLASSES = {
        FIREFOX: FirefoxTestCase,
        CHROME: ChromeTestCase,
        SAFARI: SafariTestCase,
        IE: IETestCase,
        EDGE: EdgeTestCase,
        CHROME_MOBILE: ChromeMobileTestCase,
    }
    #: List of :class:`WebDriverTestCase
    #: <webdriver_test_tools.testcase.webdriver.WebDriverTestCase>` subclasses
    #: that support test execution in a headless browser
    HEADLESS_COMPATIBLE = [
        FirefoxTestCase,
        ChromeTestCase,
        ChromeMobileTestCase,
    ]

