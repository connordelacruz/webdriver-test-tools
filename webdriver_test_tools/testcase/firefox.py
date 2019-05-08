from .webdriver import *
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class FirefoxTestCase(WebDriverTestCase):
    """Implementation of :class:`WebDriverTestCase
    <webdriver_test_tools.testcase.webdriver.WebDriverTestCase>` using Firefox
    webdriver

    `Driver download <https://github.com/mozilla/geckodriver/releases>`__

    This driver supports headless browsing:

        `Headless browser info
        <https://developer.mozilla.org/en-US/Firefox/Headless_mode>`__
    """
    DRIVER_NAME = 'Firefox'
    SHORT_NAME = DRIVER_NAME.lower()
    CAPABILITIES = DesiredCapabilities.FIREFOX.copy()

    def driver_init(self):
        return self.WebDriverConfig.get_firefox_driver(self.ENABLE_HEADLESS)

