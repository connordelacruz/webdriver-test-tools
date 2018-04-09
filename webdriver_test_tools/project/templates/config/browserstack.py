from webdriver_test_tools.config import browserstack
from webdriver_test_tools.classes.webdriver_test_case import *


# TODO: document when everything is in place
class BrowserStackConfig(browserstack.BrowserStackConfig):
    """Configurations for BrowserStack testing"""

    # Set to True to enable BrowserStack testing
    ENABLE = False
    # Account username. Projects will need to override this
    USERNAME = ''
    # Access key. Projects will need to override this
    ACCESS_KEY = ''

    # BrowserStack test configurations
    BS_CAPABILITIES = {
        'project': '', # TODO: Jinja template with project name
        # 'build': '',
        # 'browserstack.video': True,
        # 'browserstack.selenium_version': version.__selenium__, # TODO: jinja
    }

    # Configure available browsers
    # TODO: default to BrowserConfig.BROWSER_TEST_CLASSES
    BROWSER_TEST_CLASSES = {
        Browsers.FIREFOX: FirefoxTestCase,
        Browsers.CHROME: ChromeTestCase,
        # Browsers.SAFARI: SafariTestCase,
        # Browsers.IE: IETestCase,
        # Browsers.EDGE: EdgeTestCase,
        # Browsers.CHROME_MOBILE: ChromeMobileTestCase,
    }



