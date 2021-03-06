from selenium.webdriver.common.by import By
from webdriver_test_tools.pageobject import *
from webdriver_test_tools.webdriver import actions, locate

from no_yaml_example.config import SiteConfig


class FullURLExampleWebPage(prototypes.WebPageObject):
    """Non-YAML WebPageObject example (full URL)"""
    # Full URL of the page
    PAGE_URL = 'http://example.com/'


class RelativeURLExampleWebPage(prototypes.WebPageObject):
    """Non-YAML WebPageObject example (relative URL)"""
    # File name of the page relative to a base URL declared in SiteConfig
    PAGE_FILENAME = 'page.html'
    # Full URL of the page
    PAGE_URL = SiteConfig.BASE_URL + PAGE_FILENAME
