from webdriver_test_tools.testcase.browsers import *


class BrowserConfig:
    """Configurations for which browsers to generate tests for

    :var BrowserConfig.ENABLED_BROWSERS: Dictionary mapping browser names to a boolean.
        True enables the browser, False disables it. Defaults to Chrome and
        Firefox since they're not platform specific
    """

    ENABLED_BROWSERS = {
        Browsers.FIREFOX: True,
        Browsers.CHROME: True,
        Browsers.SAFARI: False,
        Browsers.IE: False,
        Browsers.EDGE: False,
        Browsers.CHROME_MOBILE: False,
    }

    @classmethod
    def get_browser_classes(cls, browser_names=None):
        """Get a list of enabled browser classes

        :param browser_names: (Optional) List of browser names to get classes for

        :return: List of enabled browser test case classes
        """
        if browser_names is None:
            browser_names = cls.ENABLED_BROWSERS.keys()
        else:
            # Use only valid browser names
            browser_names = [
                browser_name for browser_name in browser_names
                if browser_name in cls.ENABLED_BROWSERS.keys()
            ]
        browser_classes = [
            browser_class for short_name, browser_class in Browsers.TEST_CLASSES.items()
            if short_name in browser_names and cls.ENABLED_BROWSERS[short_name]
        ]
        return browser_classes

    @classmethod
    def get_browser_names(cls):
        """Returns a list of short names for enabled browser classes

        :return: List of short names for enabled browser test case classes
        """
        return [
            browser_name for browser_name, is_enabled in cls.ENABLED_BROWSERS.items()
            if is_enabled
        ]


class BrowserStackConfig(BrowserConfig):
    """Global configurations for BrowserStack testing

    :var BrowserStackConfig.ENABLE: Set to True to enable BrowserStack testing
    :var BrowserStackConfig.USERNAME: Account username. Projects will need to override this
    :var BrowserStackConfig.ACCESS_KEY: Access key. Projects will need to override this
    :var BrowserStackConfig.BS_CAPABILITIES: BrowserStack test configurations.
        `Capabilities reference <https://www.browserstack.com/automate/capabilities#>`__
    :var BrowserStackConfig.ENABLED_BROWSERS: Dictionary mapping browser names to a boolean.
        True enables the browser, False disables it. Defaults to Chrome and
        Firefox since they're not platform specific
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

        :return: Command executor URL formatted with :attr:`USERNAME` and :attr:`ACCESS_KEY`
        """
        if not cls.USERNAME or not cls.ACCESS_KEY:
            raise Exception('USERNAME or ACCESS_KEY not set in BrowserStackConfig')
        url_format = 'http://{USERNAME}:{ACCESS_KEY}@hub.browserstack.com:80/wd/hub'
        command_executor = url_format.format(USERNAME=cls.USERNAME, ACCESS_KEY=cls.ACCESS_KEY)
        return command_executor

    @classmethod
    def add_browserstack_capabilities(cls, desired_capabilities):
        """Update a desired capabilities dictionary to include items from :attr:`BS_CAPABILITIES`

        :param desired_capabilities: Desired capabilities dictionary to update
        """
        desired_capabilities.update(cls.BS_CAPABILITIES)

    @classmethod
    def update_configurations(cls, **capabilities):
        """Update BrowserStack configurations at runtime

        :param \**capabilities: Keyword arguments for BrowserStack configurations.
            Possible arguments include:

                - ``build`` (string) - Name for the group of tests
                - ``video`` (boolean) - True to enable video recording, False to disable it
        """
        caps_map = {
            'build': 'build',
            'video': 'browserstack.video',
        }
        capabilities = {k: v for k, v in capabilities.items() if k in caps_map}
        for capability, value in capabilities.items():
            cls.BS_CAPABILITIES[caps_map[capability]] = value

