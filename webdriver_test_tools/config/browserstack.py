from webdriver_test_tools.classes.webdriver_test_case import *
from webdriver_test_tools import version


class BrowserStackConfig(object):
    """Global configurations for BrowserStack testing

    :var BrowserStackConfig.ENABLE: Set to True to enable BrowserStack testing
    :var BrowserStackConfig.USERNAME: Account username. Projects will need to override this
    :var BrowserStackConfig.ACCESS_KEY: Access key. Projects will need to override this
    :var BrowserStackConfig.BS_CAPABILITIES: BrowserStack test configurations
        `Capabilities reference <https://www.browserstack.com/automate/capabilities#>`__
    :var BrowserStackConfig.BROWSER_TEST_CLASSES: Dictionary of browser test case classes to
        use indexed by the short name for that class (i.e. its command line argument).
    """

    ENABLE = False
    USERNAME = None
    ACCESS_KEY = None

    BS_CAPABILITIES = {
        'project': None,
        'browserstack.video': False,
        # 'browserstack.selenium_version': version.__selenium__,
    }

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
    def add_browserstack_capabilities(cls, desired_capabilities):
        """Update a desired capabilities dictionary to include items from BS_CAPABILITIES

        :param desired_capabilities: Desired capabilities dictionary to update
        """
        desired_capabilities.update(cls.BS_CAPABILITIES)


