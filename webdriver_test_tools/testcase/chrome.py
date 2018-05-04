from .webdriver import *
from webdriver_test_tools.config import WebDriverConfig
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class ChromeTestCase(WebDriverTestCase):
    """Implementation of WebDriverTestCase using Chrome webdriver

    `Driver download <https://sites.google.com/a/chromium.org/chromedriver/downloads>`__

    This driver supports headless browsing:

        `Headless browser info <https://developers.google.com/web/updates/2017/04/headless-chrome>`__
    """
    DRIVER_NAME = 'Chrome'
    SHORT_NAME = DRIVER_NAME.lower()
    CAPABILITIES = DesiredCapabilities.CHROME.copy()

    def driver_init(self):
        return self.WebDriverConfig.get_chrome_driver(self.ENABLE_HEADLESS)


# Mobile browser emulation

class ChromeMobileTestCase(WebDriverMobileTestCase):
    """Implementation of WebDriverTestCase using Chrome webdriver. Emulates mobile
    device layout.

    `Driver download <https://sites.google.com/a/chromium.org/chromedriver/downloads>`__

    `Mobile emulation info <https://sites.google.com/a/chromium.org/chromedriver/mobile-emulation>`__
    """
    DRIVER_NAME = 'Chrome Mobile [Emulated]'
    SHORT_NAME = 'chrome-mobile'
    CAPABILITIES = DesiredCapabilities.CHROME.copy()
    # Set options for mobile emulation
    CAPABILITIES['chromeOptions'] = {
        'mobileEmulation': WebDriverConfig.CHROME_MOBILE_EMULATION,
    }

    def driver_init(self):
        return self.WebDriverConfig.get_chrome_mobile_driver(self.ENABLE_HEADLESS)



