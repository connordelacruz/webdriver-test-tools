from .webdriver import *
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class EdgeTestCase(WebDriverTestCase):
    """Implementation of :class:`WebDriverTestCase <webdriver_test_tools.testcase.webdriver.WebDriverTestCase>`
    using Edge webdriver

    `Driver download <https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/>`_

    .. note::

        This driver is platform-specific, so it is disabled by default. It can
        be enabled in ``<test_package>/config/browser.py`` by setting the
        corresponding value in :attr:`BrowserConfig.ENABLED_BROWSERS
        <webdriver_test_tools.config.browser.BrowserConfig.ENABLED_BROWSERS>`
        to ``True``.
    """
    DRIVER_NAME = 'Edge'
    SHORT_NAME = DRIVER_NAME.lower()
    CAPABILITIES = DesiredCapabilities.EDGE.copy()
    # Set version
    CAPABILITIES['version'] = '16'

    def driver_init(self):
        return self.WebDriverConfig.get_edge_driver()


