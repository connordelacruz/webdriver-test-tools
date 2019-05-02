import os

from selenium.webdriver.common.by import By
from webdriver_test_tools.pageobject import *
from webdriver_test_tools.webdriver import actions, locate

from yaml_example.config import SiteConfig


class ExampleNav(prototypes.NavObject):
    """YAML NavObject example"""

    # Path to YAML file representing the object
    YAML_FILE = os.path.join(os.path.dirname(__file__), 'nav.yml')

    # Used for internal methods (do not modify)
    SITE_CONFIG = SiteConfig

