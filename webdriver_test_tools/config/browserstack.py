from webdriver_test_tools.classes.webdriver_test_case import *
from webdriver_test_tools import version


# TODO: document when everything is in place
class BrowserStackConfig(object):
    """Configurations for BrowserStack testing"""

    # Set to True to enable BrowserStack testing
    ENABLE = False
    # Account username. Projects will need to override this
    USERNAME = None
    # Access key. Projects will need to override this
    ACCESS_KEY = None

    # BrowserStack test configurations
    BS_CAPABILITIES = {
        'project': None,
        'build': None,
        'browserstack.video': True,
        # 'browserstack.selenium_version': version.__selenium__, # TODO: implement
    }

    # Configure available browsers
    BROWSER_TEST_CLASSES = {
        Browsers.FIREFOX: FirefoxTestCase,
        Browsers.CHROME: ChromeTestCase,
        # Browsers.SAFARI: SafariTestCase,
        # Browsers.IE: IETestCase,
        # Browsers.EDGE: EdgeTestCase,
        # Browsers.CHROME_MOBILE: ChromeMobileTestCase,
    }

    # Methods

    @classmethod
    def get_command_executor(cls):
        """Returns the command executor URL

        :return: Command executor URL formatted with USERNAME and ACCESS_KEY
        """
        if not cls.USERNAME or not cls.ACCESS_KEY:
            raise Exception('USERNAME or ACCESS_KEY not set in BrowserStackConfig')
        url_format = 'http://{USERNAME}:{ACCESS_KEY}@hub.browserstack.com:80/wd/hub'
        command_executor = url_format.format(USERNAME=cls.USERNAME, ACCESS_KEY=cls.ACCESS_KEY)
        return command_executor

    @classmethod
    def set_browserstack_capabilities(cls, desired_capabilities):
        """Update a desired capabilities dictionary to include items from BS_CAPABILITIES

        :param desired_capabilities: Desired capabilities dictionary to update
        """
        desired_capabilities.update(cls.BS_CAPABILITIES)


