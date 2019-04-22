import os

from selenium.webdriver.common.by import By
from webdriver_test_tools.pageobject import *
from webdriver_test_tools.webdriver import actions, locate

from page_object_tests.config import SiteConfig


class YAMLRelativeWebPageObject(prototypes.WebPageObject):

    # Path to YAML file representing the object
    YAML_FILE = os.path.join(os.path.dirname(__file__), 'yaml_relative_web_page.yml')

    # Used for internal WebPageObject methods (do not modify)
    SITE_CONFIG = SiteConfig

class YAMLFullURLWebPageObject(prototypes.WebPageObject):

    # Path to YAML file representing the object
    YAML_FILE = os.path.join(os.path.dirname(__file__), 'yaml_full_url_web_page.yml')

    # Used for internal WebPageObject methods (do not modify)
    SITE_CONFIG = SiteConfig

