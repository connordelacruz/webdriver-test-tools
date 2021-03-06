import os
from webdriver_test_tools.config import browserstack
from webdriver_test_tools.testcase.browsers import *


class BrowserStackConfig(browserstack.BrowserStackConfig):
    """Configurations for BrowserStack testing"""

    # Required Configurations

    # (Default = False) Set to True to enable BrowserStack testing
    ENABLE = False

    # Account username. Required for BrowserStack testing.
    # Uses the value of BROWSERSTACK_USERNAME environment variable by default
    USERNAME = os.getenv('BROWSERSTACK_USERNAME', '')

    # Access key. Required for BrowserStack testing.
    # Uses the value of BROWSERSTACK_ACCESS_KEY environment variable by 
    # default
    ACCESS_KEY = os.getenv('BROWSERSTACK_ACCESS_KEY', '')


    # Browsers

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


    # Advanced Configurations

    # BrowserStack test configurations
    BS_CAPABILITIES = {
        'project': 'page_object_tests',
        'browserstack.video': False,
        # 'browserstack.selenium_version': '3.11.0',
    }
