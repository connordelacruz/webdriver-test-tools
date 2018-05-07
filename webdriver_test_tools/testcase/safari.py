from .webdriver import *
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class SafariTestCase(WebDriverTestCase):
    """Implementation of WebDriverTestCase using Safari webdriver

    `Driver info <https://webkit.org/blog/6900/webdriver-support-in-safari-10/>`__

    .. warning::

        This class is experimental and has not been fully tested. It is disabled by
        default but can be enabled in ``<test_package>/config/browser.py`` by
        setting the corresponding value in ``BrowserConfig.ENABLED_BROWSERS`` to ``True``.

    .. warning::

        Safari's webdriver is missing certain features of the webdriver API, which can
        cause test failures. As of Safari 11.0.3, issues with the following modules
        have been encountered during testing:

            - ``selenium.webdriver.common.action_chains``
            - ``selenium.webdriver.support.select``
    """
    DRIVER_NAME = 'Safari'
    SHORT_NAME = DRIVER_NAME.lower()
    CAPABILITIES = DesiredCapabilities.SAFARI.copy()

    def driver_init(self):
        return self.WebDriverConfig.get_safari_driver()


