import os

from selenium.webdriver.common.by import By
from webdriver_test_tools.pageobject import *
from webdriver_test_tools.webdriver import actions, locate

from page_object_tests.config import SiteConfig


# YAML

class YAMLWebPageRelative(prototypes.WebPageObject):

    # Path to YAML file representing the object
    YAML_FILE = os.path.join(os.path.dirname(__file__), 'web_page_relative.yml')

    # Used for internal WebPageObject methods (do not modify)
    SITE_CONFIG = SiteConfig

class YAMLWebPageFullURL(prototypes.WebPageObject):

    # Path to YAML file representing the object
    YAML_FILE = os.path.join(os.path.dirname(__file__), 'web_page_full_url.yml')

    # Used for internal WebPageObject methods (do not modify)
    SITE_CONFIG = SiteConfig


# No YAML

class NoYAMLWebPage(prototypes.WebPageObject):

    # File name of the page relative to a base URL declared in SiteConfig
    PAGE_FILENAME = 'domains/reserved'
    # Full URL of the page. E.g.:
    # PAGE_URL = SiteConfig.BASE_URL + PAGE_FILENAME
    PAGE_URL = SiteConfig.IANA_BASE_URL + PAGE_FILENAME

