import os

from selenium.webdriver.common.by import By
from webdriver_test_tools.pageobject import *
from webdriver_test_tools.webdriver import actions, locate

from page_object_tests.config import SiteConfig


class YAMLNavObject(prototypes.NavObject):

    PAGE_FILENAME = 'navbar.html'

    class Locator:
        """WebDriver locator tuples for any elements that will need to be
        accessed by this page object.
        """
        pass

    # SET THE FOLLOWING ATTRIBUTES TO USE IN NavObject METHODS

    # Path to YAML file representing the object
    YAML_FILE = os.path.join(os.path.dirname(__file__), 'yaml_nav.yml')

    # Used for internal methods (do not modify)
    SITE_CONFIG = SiteConfig


