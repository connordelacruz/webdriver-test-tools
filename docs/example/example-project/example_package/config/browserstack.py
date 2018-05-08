from webdriver_test_tools.config import browserstack
from webdriver_test_tools.testcase.browsers import *


class BrowserStackConfig(browserstack.BrowserStackConfig):
    """Configurations for BrowserStack testing

    :var BrowserStackConfig.ENABLE: (Default = False) Set to True to enable BrowserStack testing
    :var BrowserStackConfig.USERNAME: Account username. Required for BrowserStack testing
    :var BrowserStackConfig.ACCESS_KEY: Access key. Required for BrowserStack testing
    :var BrowserStackConfig.BS_CAPABILITIES: BrowserStack test configurations
    :var BrowserConfig.ENABLED_BROWSERS: Dictionary mapping browser names to a boolean.
        True enables the browser, False disables it. Defaults to Chrome and
        Firefox since they're not platform specific
    """

    ENABLE = False
    USERNAME = ''
    ACCESS_KEY = ''

    BS_CAPABILITIES = {
        'project': 'example_package',
        'browserstack.video': False,
        # 'browserstack.selenium_version': '3.11.0',
    }

    ENABLED_BROWSERS = {
        Browsers.FIREFOX: True,
        Browsers.CHROME: True,
        Browsers.SAFARI: False,
        Browsers.IE: False,
        Browsers.EDGE: False,
        Browsers.CHROME_MOBILE: False,
    }


