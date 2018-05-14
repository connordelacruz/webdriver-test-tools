"""Default configurations for various items in the test framework

Config Classes
==============

.. autoclass:: webdriver_test_tools.config.browser.BrowserConfig
    :members:
    :undoc-members:
    :noindex:

.. autoclass:: webdriver_test_tools.config.browser.BrowserStackConfig
    :members:
    :undoc-members:
    :noindex:

.. autoclass:: webdriver_test_tools.config.site.SiteConfig
    :members:
    :undoc-members:
    :noindex:

.. autoclass:: webdriver_test_tools.config.test.TestSuiteConfig
    :members:
    :undoc-members:
    :noindex:

.. autoclass:: webdriver_test_tools.config.webdriver.WebDriverConfig
    :members:
    :undoc-members:
    :exclude-members: LOG_PATH, SCREENSHOT_PATH
    :noindex:

"""
from .site import SiteConfig
from .test import TestSuiteConfig
from .webdriver import WebDriverConfig
from .browser import BrowserConfig, BrowserStackConfig

