from webdriver_test_tools.classes.webdriver_test_case import *


class BrowserConfig(object):
    """Configurations for what browsers to generate tests for

    :var BrowserConfig.BROWSER_TEST_CLASSES: Dictionary of browser test case classes to
        use indexed by the short name for that class (i.e. its command line argument).
        Default to Chrome and Firefox since they're not platform specific
    """
    BROWSER_TEST_CLASSES = {
        Browsers.FIREFOX: FirefoxTestCase,
        Browsers.CHROME: ChromeTestCase,
        # Browsers.SAFARI: SafariTestCase,
        # Browsers.IE: IETestCase,
        # Browsers.EDGE: EdgeTestCase,
        # Browsers.CHROME_MOBILE: ChromeMobileTestCase,
    }

    class Browsers(Browsers):
        """Attribute that mirrors the content of :class:`webdriver_test_tools.classes.webdriver_test_case.Browsers`
        for convenience
        """
        pass

