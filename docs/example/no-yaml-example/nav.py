from selenium.webdriver.common.by import By
from webdriver_test_tools.pageobject import *
from webdriver_test_tools.webdriver import actions, locate

from no_yaml_example.config import SiteConfig


class ExampleNavObject(prototypes.NavObject):
    """Non-YAML NavObject example"""

    # Used for internal methods (do not modify)
    SITE_CONFIG = SiteConfig

    # (Default = True) Whether the navbar is fixed to the window
    FIXED = False

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
        # Dropdown menu (hover):
        {
            'name': 'hover-menu',
            'link_locator': (By.ID, 'hover-menu-link'),
            # Set click action to 'none' (unless link also has a click action)
            'click': 'none',
            # Set hover action to 'menu'
            'hover': 'menu',
            'menu': [
                'menu_locator': (By.ID, 'hover-menu'),
                # Dropdown menu links (same syntax as nav links):
                'links': [
                    {
                        'name': 'page1',
                        'link_locator': (By.CSS_SELECTOR, '#hover-menu a[href="page1.html"]'),
                        'target': SITE_CONFIG.BASE_URL + 'page1.html'
                    },
                    {
                        'name': 'page2',
                        'link_locator': (By.CSS_SELECTOR, '#hover-menu a[href="page2.html"]'),
                        'target': SITE_CONFIG.BASE_URL + 'page2.html'
                    },
                ]
            ]
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

