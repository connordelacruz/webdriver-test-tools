# TODO: document
# TODO: make a template config for this for projects to override
from webdriver_test_tools.classes.webdriver_test_case import *

class Browsers(object):
    FIREFOX = FirefoxTestCase.SHORT_NAME
    CHROME = ChromeTestCase.SHORT_NAME
    SAFARI = SafariTestCase.SHORT_NAME
    IE = IETestCase.SHORT_NAME
    EDGE = EdgeTestCase.SHORT_NAME


# Dictionary of usable test case classes indexed by the short name for that class (i.e. its command line argument)
BROWSER_TEST_CLASSES = {
    Browsers.FIREFOX: FirefoxTestCase,
    Browsers.CHROME: ChromeTestCase,
    Browsers.SAFARI: SafariTestCase,
    Browsers.IE: IETestCase,
    Browsers.EDGE: EdgeTestCase,
}

