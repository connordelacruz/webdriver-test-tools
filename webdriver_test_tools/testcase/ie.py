from .webdriver import *
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class IETestCase(WebDriverTestCase):
    """Implementation of :class:`WebDriverTestCase
    <webdriver_test_tools.testcase.webdriver.WebDriverTestCase>` using Internet
    Explorer webdriver

    `Driver info
    <https://github.com/SeleniumHQ/selenium/wiki/InternetExplorerDriver>`__

    .. note::

        This driver is platform-specific, so it is disabled by default. It can
        be enabled in ``<test_package>/config/browser.py`` by setting the
        corresponding value in :attr:`BrowserConfig.ENABLED_BROWSERS
        <webdriver_test_tools.config.browser.BrowserConfig.ENABLED_BROWSERS>`
        to ``True``.
    """
    DRIVER_NAME = 'Internet Explorer'
    SHORT_NAME = 'ie'
    CAPABILITIES = DesiredCapabilities.INTERNETEXPLORER.copy()
    # Set version
    CAPABILITIES['version'] = '11'

    def driver_init(self):
        return self.WebDriverConfig.get_ie_driver()
