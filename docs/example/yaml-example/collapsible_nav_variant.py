import os

from selenium.webdriver.common.by import By
from webdriver_test_tools.pageobject import *
from webdriver_test_tools.webdriver import actions, locate

# 1. Import the non-collapsible nav object
from yaml_example.pages.nav import ExampleNav


# 2. Subclass non-collapsible nav
class ExampleCollapsibleVariantNav(ExampleNavObject):
    """Collapsible NavObject from non-collapsible example"""
    # 3. Set collapsible attributes
    COLLAPSIBLE = True
    MENU_LOCATOR = (By.ID, 'nav-menu')
    EXPAND_BUTTON_LOCATOR = (By.ID, 'navbar-toggle')

