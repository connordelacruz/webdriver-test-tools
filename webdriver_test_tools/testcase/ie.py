from .webdriver import *
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class IETestCase(WebDriverTestCase):
    """Implementation of WebDriverTestCase using Internet Explorer webdriver

    `Driver info <https://github.com/SeleniumHQ/selenium/wiki/InternetExplorerDriver>`__

    .. warning::

        This class is experimental and has not been fully tested. It is disabled by
        default but can be enabled in ``<test_package>/config/browser.py`` by
        setting the corresponding value in ``BrowserConfig.ENABLED_BROWSERS`` to ``True``.
    """
    DRIVER_NAME = 'Internet Explorer'
    SHORT_NAME = 'ie'
    CAPABILITIES = DesiredCapabilities.INTERNETEXPLORER.copy()
    # Set version
    CAPABILITIES['version'] = '11'

    def driver_init(self):
        return self.WebDriverConfig.get_ie_driver()
