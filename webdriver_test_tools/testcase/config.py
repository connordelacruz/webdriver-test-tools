from .browsers import *


class Browsers:
    """Constants for browser short names

    :var Browsers.HEADLESS_COMPATIBLE: List of WebDriverTestCase subclasses that
        support test execution in a headless browser
    """
    FIREFOX = FirefoxTestCase.SHORT_NAME
    CHROME = ChromeTestCase.SHORT_NAME
    SAFARI = SafariTestCase.SHORT_NAME
    IE = IETestCase.SHORT_NAME
    EDGE = EdgeTestCase.SHORT_NAME
    CHROME_MOBILE = ChromeMobileTestCase.SHORT_NAME
    # List of browser classes that support headless browsing
    HEADLESS_COMPATIBLE = [
        FirefoxTestCase,
        ChromeTestCase,
        ChromeMobileTestCase,
    ]

class BrowserConfig:
    """Configurations for what browsers to generate tests for

    :var BrowserConfig.BROWSER_TEST_CLASSES: Dictionary of browser test case classes to
        use indexed by the short name for that class (i.e. its command line argument).
        Default to Chrome and Firefox since they're not platform specific
    """
    # TODO: move this to Browsers?
    BROWSER_TEST_CLASSES = {
        Browsers.FIREFOX: FirefoxTestCase,
        Browsers.CHROME: ChromeTestCase,
        Browsers.SAFARI: SafariTestCase,
        Browsers.IE: IETestCase,
        Browsers.EDGE: EdgeTestCase,
        Browsers.CHROME_MOBILE: ChromeMobileTestCase,
    }

    ENABLED_BROWSERS = {
        Browsers.FIREFOX: True,
        Browsers.CHROME: True,
        Browsers.SAFARI: False,
        Browsers.IE: False,
        Browsers.EDGE: False,
        Browsers.CHROME_MOBILE: False,
    }

    @classmethod
    def get_browser_classes(cls):
        """Get a list of enabled browser classes

        :return: List of enabled browser test case classes
        """
        browser_classes = [
            browser_class for short_name, browser_class in cls.BROWSER_TEST_CLASSES.items()
            if short_name in cls.ENABLED_BROWSERS and cls.ENABLED_BROWSERS[short_name]
        ]
        return browser_classes


class BrowserStackConfig(BrowserConfig):
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

