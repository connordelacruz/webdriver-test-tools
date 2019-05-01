import os

from selenium.webdriver.common.by import By
from webdriver_test_tools.pageobject import *
from webdriver_test_tools.webdriver import actions, locate

from yaml_example.config import SiteConfig


class FullURLExampleWebPageObject(prototypes.WebPageObject):
    """YAML WebPageObject example (full URL)"""

    # Path to YAML file representing the object
    YAML_FILE = os.path.join(os.path.dirname(__file__), 'web_page_full.yml')
    # Used for internal methods (do not modify)
    SITE_CONFIG = SiteConfig


class RelativeURLExampleWebPageObject(prototypes.WebPageObject):
    """YAML WebPageObject example (relative URL)"""

    # Path to YAML file representing the object
    YAML_FILE = os.path.join(os.path.dirname(__file__), 'web_page_relative.yml')
    # Used for internal methods (do not modify)
    SITE_CONFIG = SiteConfig
