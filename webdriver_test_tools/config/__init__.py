"""Default configurations for various items in the test framework.

This module imports the following classes:

    :class:`webdriver_test_tools.config.browser.BrowserConfig`
    :class:`webdriver_test_tools.config.browser.BrowserStackConfig`
    :class:`webdriver_test_tools.config.projectfiles.ProjectFilesConfig`
    :class:`webdriver_test_tools.config.site.SiteConfig`
    :class:`webdriver_test_tools.config.test.TestSuiteConfig`
    :class:`webdriver_test_tools.config.webdriver.WebDriverConfig`

.. toctree::

   webdriver_test_tools.config.browser
   webdriver_test_tools.config.browserstack
   webdriver_test_tools.config.projectfiles
   webdriver_test_tools.config.site
   webdriver_test_tools.config.test
   webdriver_test_tools.config.webdriver
"""
from .projectfiles import ProjectFilesConfig
from .site import SiteConfig
from .test import TestSuiteConfig
from .webdriver import WebDriverConfig
from .browser import BrowserConfig, BrowserStackConfig

