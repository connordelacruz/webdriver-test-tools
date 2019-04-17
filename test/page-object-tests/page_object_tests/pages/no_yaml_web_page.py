from selenium.webdriver.common.by import By
from webdriver_test_tools.pageobject import *
from webdriver_test_tools.webdriver import actions, locate

from page_object_tests.config import SiteConfig


class NoYAMLWebPageObject(prototypes.WebPageObject):

    class Locator:
        """WebDriver locator tuples for any elements that will need to be
        accessed by this page object.
        """
        pass

    # File name of the page relative to a base URL declared in SiteConfig
    PAGE_FILENAME = 'domains/reserved'
    # Full URL of the page. E.g.:
    # PAGE_URL = SiteConfig.BASE_URL + PAGE_FILENAME
    PAGE_URL = SiteConfig.IANA_BASE_URL + PAGE_FILENAME
