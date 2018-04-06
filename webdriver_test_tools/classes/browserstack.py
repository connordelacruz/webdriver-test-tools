"""BrowserStack driver classes"""
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_test_tools.classes.webdriver_test_case import WebDriverTestCase


# Constants

class Capabilities(object):
    """Constants for supported WebDriver desired_capabilities

    `BrowserStack Capabilities Reference <https://www.browserstack.com/automate/capabilities>`__
    """

    # TODO: Add other capabilities?
    # TODO: Just use BrowserStack specific capabilities?

    class Platform(object):
        MAC = 'MAC'
        WIN8 = 'WIN8'
        XP = 'XP'
        WINDOWS = 'WINDOWS'
        ANY = 'ANY'
        ANDROID = 'ANDROID'

    class BrowserName(object):
        FIREFOX = 'firefox'
        CHROME = 'chrome'
        IE = 'internet explorer'
        SAFARI = 'safari'
        OPERA = 'opera'
        EDGE = 'edge'
        IPAD = 'iPad'
        IPHONE = 'iPhone'
        ANDROID = 'android'


# Test Case Classes

class BrowserStackTestCase(WebDriverTestCase):
    # TODO: document

    # TODO: figure out how this is going to work
    # Command executor URL. Test projects need to set this with their access key and username
    COMMAND_EXECUTOR = None
    # Desired capabilities for the driver. Browser implementations override this
    CAPABILITIES = None

    def setUp(self):
        self.driver = webdriver.Remote(command_executor=self.COMMAND_EXECUTOR,
                desired_capabilities=self.CAPABILITIES)
        super().setUp()


# Browser implementations

class BSChromeTestCase(BrowserStackTestCase):
    """Implementation of BrowserStackTestCase using Chrome"""
    CAPABILITIES = DesiredCapabilities.CHROME


