from webdriver_test_tools.config import browserstack
from webdriver_test_tools.classes.webdriver_test_case import *
from test_project.config import BrowserConfig


class BrowserStackConfig(browserstack.BrowserStackConfig):
    """Configurations for BrowserStack testing

    :var BrowserStackConfig.ENABLE: (Default = False) Set to True to enable BrowserStack testing
    :var BrowserStackConfig.USERNAME: Account username. Required for BrowserStack testing
    :var BrowserStackConfig.ACCESS_KEY: Access key. Required for BrowserStack testing
    :var BrowserStackConfig.BS_CAPABILITIES: BrowserStack test configurations
    :var BrowserStackConfig.BROWSER_TEST_CLASSES: Dictionary of browser test case classes to
        use indexed by the short name for that class (i.e. its command line argument).
    """

    ENABLE = False
    USERNAME = ''
    ACCESS_KEY = ''

    BS_CAPABILITIES = {
        'project': 'test_project',
        'browserstack.video': False,
        # 'browserstack.selenium_version': '3.11.0',
    }

    # Defaults to using the same browsers configured in BrowserConfig class
    BROWSER_TEST_CLASSES = BrowserConfig.BROWSER_TEST_CLASSES.copy()
    # Add additional browsers here:
    _additional_browsers = {
        # Browsers.FIREFOX: FirefoxTestCase,
        # Browsers.CHROME: ChromeTestCase,
        # Browsers.SAFARI: SafariTestCase,
        # Browsers.IE: IETestCase,
        # Browsers.EDGE: EdgeTestCase,
        # Browsers.CHROME_MOBILE: ChromeMobileTestCase,
    }
    BROWSER_TEST_CLASSES.update(_additional_browsers)


