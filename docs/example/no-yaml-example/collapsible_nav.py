from selenium.webdriver.common.by import By
from webdriver_test_tools.pageobject import *
from webdriver_test_tools.webdriver import actions, locate

from no_yaml_example.config import SiteConfig


class ExampleCollapsibleNav(prototypes.NavObject):
    """Non-YAML collapsible NavObject example"""

    # Used for internal methods (do not modify)
    SITE_CONFIG = SiteConfig

    COLLAPSIBLE = True
    # REQUIRED: Locator for the collapsible menu element
    MENU_LOCATOR = (By.ID, 'nav-menu')
    # REQUIRED: Locator for the button that expands the nav menu
    EXPAND_BUTTON_LOCATOR = (By.ID, 'navbar-toggle')
    # Expand and collapse button are the same in this example
    # COLLAPSE_BUTTON_LOCATOR = None

    # Links are specified here:
    LINK_DICTS = [
        # Page link:
        {
            'name': 'home',
            'link_locator': (By.CLASS_NAME, 'navbar-brand'),
            'target': SITE_CONFIG.BASE_URL + 'index.html'
        },
        # Section link:
        {
            'name': 'section1',
            'link_locator': (By.CSS_SELECTOR, 'a[href="#section1"]'),
            'click': 'section',
            'target': '#section1'
        },
        # Dropdown menu (click):
        {
            'name': 'click-menu',
            'link_locator': (By.ID, 'click-menu-link'),
            # Set click action to 'menu'
            'click': 'menu',
            'menu': [
                'menu_locator': (By.ID, 'click-menu'),
                # Dropdown menu links (same syntax as nav links):
                'links': [
                    {
                        'name': 'page1',
                        'link_locator': (By.CSS_SELECTOR, '#click-menu a[href="page1.html"]'),
                        'target': SITE_CONFIG.BASE_URL + 'page1.html'
                    },
                    {
                        'name': 'page2',
                        'link_locator': (By.CSS_SELECTOR, '#click-menu a[href="page2.html"]'),
                        'target': SITE_CONFIG.BASE_URL + 'page2.html'
                    },
                ]
            ]
        },
    ]

