from webdriver_test_tools.testcase.browsers import *
from webdriver_test_tools.config import browser


class BrowserConfig(browser.BrowserConfig):
    """Configurations for which browsers to generate tests for"""

    # Dictionary mapping browser names to a boolean. True enables the browser,
    # False disables it. Defaults to Chrome and Firefox since they're not
    # platform specific
    ENABLED_BROWSERS = {
        Browsers.FIREFOX: True,
        Browsers.CHROME: True,
        Browsers.SAFARI: False,
        Browsers.IE: False,
        Browsers.EDGE: False,
        Browsers.CHROME_MOBILE: False,
    }
