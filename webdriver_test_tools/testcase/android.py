from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from .webdriver import WebDriverMobileTestCase


class AndroidTestCase(WebDriverMobileTestCase):
    # TODO: document
    DRIVER_NAME = 'Android'
    SHORT_NAME = DRIVER_NAME.lower()
    CAPABILITIES = DesiredCapabilities.ANDROID.copy()

    def driver_init(self):
        # TODO: exception (currently BrowserStack only)
        pass

    def bs_driver_init(self):
        # TODO: document
        self.CAPABILITIES['realMobile'] = 'true'
        # TODO: Get values from self.WebDriverConfig
        _capabilities = {
            'device': 'Google Pixel',
            'os_version': '8.0',
        }
        self.CAPABILITIES.update(_capabilities)
        return super().bs_driver_init()



