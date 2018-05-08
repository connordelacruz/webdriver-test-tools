from .chrome import *
from .edge import *
from .firefox import *
from .ie import *
from .safari import *

class Browsers(object):
    """Constants for browser short names

    :var Browsers.TEST_CLASSES: Dictionary mapping browser names to their corresponding test classes
    :var Browsers.HEADLESS_COMPATIBLE: List of WebDriverTestCase subclasses that
        support test execution in a headless browser
    """
    FIREFOX = FirefoxTestCase.SHORT_NAME
    CHROME = ChromeTestCase.SHORT_NAME
    SAFARI = SafariTestCase.SHORT_NAME
    IE = IETestCase.SHORT_NAME
    EDGE = EdgeTestCase.SHORT_NAME
    CHROME_MOBILE = ChromeMobileTestCase.SHORT_NAME
    # Map of short names to the browser class
    TEST_CLASSES = {
        FIREFOX: FirefoxTestCase,
        CHROME: ChromeTestCase,
        SAFARI: SafariTestCase,
        IE: IETestCase,
        EDGE: EdgeTestCase,
        CHROME_MOBILE: ChromeMobileTestCase,
    }
    # List of browser classes that support headless browsing
    HEADLESS_COMPATIBLE = [
        FirefoxTestCase,
        ChromeTestCase,
        ChromeMobileTestCase,
    ]

