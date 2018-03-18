# Configurations for what browser test cases to use

from webdriver_test_tools.classes.webdriver_test_case import *
from webdriver_test_tools.config import browser
from webdriver_test_tools.config.browser import Browsers


class BrowserConfig(browser.BrowserConfig):
    # Dictionary of usable test case classes indexed by the short name for that class (i.e. its command line argument)
    BROWSER_TEST_CLASSES = {
        Browsers.FIREFOX: FirefoxTestCase,
        Browsers.CHROME: ChromeTestCase,
        # Browsers.SAFARI: SafariTestCase,
        # Browsers.IE: IETestCase,
        # Browsers.EDGE: EdgeTestCase,
    }

