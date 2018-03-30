# Configurations for what browser test cases to use

from webdriver_test_tools.classes.webdriver_test_case import *

# TODO: move to webdriver_test_tools.classes.webdriver_test_case
class Browsers(object):
    """Constants for browser short names. Used for mapping to classes in BROWSER_TEST_CLASSES"""
    FIREFOX = FirefoxTestCase.SHORT_NAME
    CHROME = ChromeTestCase.SHORT_NAME
    SAFARI = SafariTestCase.SHORT_NAME
    IE = IETestCase.SHORT_NAME
    EDGE = EdgeTestCase.SHORT_NAME


class BrowserConfig(object):
    # Dictionary of usable test case classes indexed by the short name for that class (i.e. its command line argument)
    BROWSER_TEST_CLASSES = {
        # Default to Chrome and Firefox since those aren't platform specific
        Browsers.FIREFOX: FirefoxTestCase,
        Browsers.CHROME: ChromeTestCase,
        # Browsers.SAFARI: SafariTestCase,
        # Browsers.IE: IETestCase,
        # Browsers.EDGE: EdgeTestCase,
    }

