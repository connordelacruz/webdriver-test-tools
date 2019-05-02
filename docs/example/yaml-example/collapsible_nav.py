import os

from selenium.webdriver.common.by import By
from webdriver_test_tools.pageobject import *
from webdriver_test_tools.webdriver import actions, locate

from yaml_example.config import SiteConfig


class ExampleCollapsibleNav(prototypes.NavObject):
    """YAML collapsible NavObject example"""

    # Path to YAML file representing the object
    YAML_FILE = os.path.join(os.path.dirname(__file__), 'collapsible_nav.yml')

    # Used for internal methods (do not modify)
    SITE_CONFIG = SiteConfig

