import os

from selenium.webdriver.common.by import By
from webdriver_test_tools.pageobject import *
from webdriver_test_tools.webdriver import actions, locate

from page_object_tests.config import SiteConfig


# YAML

class YAMLNav(prototypes.NavObject):
    """Regular nav object"""

    PAGE_FILENAME = 'navbar.html'

    # Path to YAML file representing the object
    YAML_FILE = os.path.join(os.path.dirname(__file__), 'nav.yml')

    # Used for internal methods (do not modify)
    SITE_CONFIG = SiteConfig


class YAMLNavFixed(prototypes.NavObject):
    """Fixed nav object"""

    PAGE_FILENAME = 'fixed_navbar.html'

    # Path to YAML file representing the object
    YAML_FILE = os.path.join(os.path.dirname(__file__), 'nav_fixed.yml')

    # Used for internal methods (do not modify)
    SITE_CONFIG = SiteConfig


# Collapsible

class YAMLCollapsibleNav(prototypes.NavObject):
    """Collapsible nav object"""

    PAGE_FILENAME = 'collapsible_navbar.html'

    # Path to YAML file representing the object
    YAML_FILE = os.path.join(os.path.dirname(__file__), 'collapsible_nav.yml')

    # Used for internal methods (do not modify)
    SITE_CONFIG = SiteConfig


class YAMLCollapsibleNavFixed(prototypes.NavObject):
    """Fixed collapsible nav object"""

    PAGE_FILENAME = 'fixed_collapsible_navbar.html'

    # Path to YAML file representing the object
    YAML_FILE = os.path.join(os.path.dirname(__file__), 'collapsible_nav_fixed.yml')

    # Used for internal methods (do not modify)
    SITE_CONFIG = SiteConfig


class YAMLNavCollapsibleSubclass(YAMLNav):
    """Collapsible nav subclassing a YAML parsing non-collapsible nav"""

    PAGE_FILENAME = 'collapsible_navbar.html'

    COLLAPSIBLE = True
    MENU_LOCATOR = (By.ID, 'nav-menu')
    EXPAND_BUTTON_LOCATOR = (By.ID, 'navbar-toggle')


# No YAML

class NoYAMLNav(prototypes.NavObject):

    # Used for internal methods (do not modify)
    SITE_CONFIG = SiteConfig

    # REQUIRED: List of link dictionaries. These will be used to initialize
    # NavLinkObject instances at runtime.
    # Dictionaries use same keys as YAML links. For syntax, see:
    # https://connordelacruz.com/webdriver-test-tools/yaml.html#yaml-links

    LINK_DICTS = [
        {
            'name': 'home',
            'link_locator': (By.CLASS_NAME, 'navbar-brand'),
            'target': SiteConfig.BASE_URL + 'index.html'
        },
        {
            'name': 'section3',
            'link_locator': (By.CSS_SELECTOR, 'a[href="#section3"]'),
            'click': 'section',
            'target': '#section3'
        },
        {
            'name': 'hover-menu',
            'link_locator': (By.ID, 'hover-menu-link'),
            'click': None,
            'hover': 'menu',
            'menu': {
                'menu_locator': (By.ID, 'hover-menu'),
                'links': [
                    {
                        'name': 'home',
                        'link_locator': (By.CSS_SELECTOR, '#hover-menu a[href="index.html"]'),
                        'target': SiteConfig.BASE_URL + 'index.html'
                    },
                    {
                        'name': 'form',
                        'link_locator': (By.CSS_SELECTOR, '#hover-menu a[href="form.html"]'),
                        'target': SiteConfig.BASE_URL + 'form.html'
                    },
                    {
                        'name': 'modal',
                        'link_locator': (By.CSS_SELECTOR, '#hover-menu a[href="modal.html"]'),
                        'target': SiteConfig.BASE_URL + 'modal.html'
                    },
                ]
            }
        },
        {
            'name': 'click-menu',
            'link_locator': (By.ID, 'click-menu-link'),
            'click': 'menu',
            'menu': {
                'menu_locator': (By.ID, 'click-menu'),
                'links': [
                    {
                        'name': 'home',
                        'link_locator': (By.CSS_SELECTOR, '#click-menu a[href="index.html"]'),
                        'target': SiteConfig.BASE_URL + 'index.html'
                    },
                    {
                        'name': 'form',
                        'link_locator': (By.CSS_SELECTOR, '#click-menu a[href="form.html"]'),
                        'target': SiteConfig.BASE_URL + 'form.html'
                    },
                    {
                        'name': 'modal',
                        'link_locator': (By.CSS_SELECTOR, '#click-menu a[href="modal.html"]'),
                        'target': SiteConfig.BASE_URL + 'modal.html'
                    },
                ]
            }
        },
    ]

    # (Default = True) True if element is a fixed navbar, False otherwise. If
    # set to False, click_page_link() and hover_over_page_link() will scroll
    # the target link into view before interacting with it
    FIXED = False


class NoYAMLNavFixed(NoYAMLNav):
    FIXED = True


class NoYAMLCollapsibleNav(prototypes.NavObject):

    # Used for internal methods (do not modify)
    SITE_CONFIG = SiteConfig

    # REQUIRED: List of link dictionaries. These will be used to initialize
    # NavLinkObject instances at runtime.
    # Dictionaries use same keys as YAML links. For syntax, see:
    # https://connordelacruz.com/webdriver-test-tools/yaml.html#yaml-links
    LINK_DICTS = [
        {
            'name': 'home',
            'link_locator': (By.CLASS_NAME, 'navbar-brand'),
            'target': SiteConfig.BASE_URL + 'index.html'
        },
        {
            'name': 'section3',
            'link_locator': (By.CSS_SELECTOR, 'a[href="#section3"]'),
            'click': 'section',
            'target': '#section3'
        },
        {
            'name': 'click-menu',
            'link_locator': (By.ID, 'click-menu-link'),
            'click': 'menu',
            'menu': {
                'menu_locator': (By.ID, 'click-menu'),
                'links': [
                    {
                        'name': 'home',
                        'link_locator': (By.CSS_SELECTOR, '#click-menu a[href="index.html"]'),
                        'target': SiteConfig.BASE_URL + 'index.html'
                    },
                    {
                        'name': 'form',
                        'link_locator': (By.CSS_SELECTOR, '#click-menu a[href="form.html"]'),
                        'target': SiteConfig.BASE_URL + 'form.html'
                    },
                    {
                        'name': 'modal',
                        'link_locator': (By.CSS_SELECTOR, '#click-menu a[href="modal.html"]'),
                        'target': SiteConfig.BASE_URL + 'modal.html'
                    },
                ]
            }
        },
    ]
    # (Default: False) Whether or not the navbar is collapsible
    COLLAPSIBLE = True
    # REQUIRED: Locator for the collapsible menu element
    MENU_LOCATOR = (By.ID, 'nav-menu')
    # REQUIRED: Locator for the button that expands the nav menu
    EXPAND_BUTTON_LOCATOR = (By.ID, 'navbar-toggle')
    # (Optional) Locator for the button that collapses the nav menu.
    # If not set, the value from EXPAND_BUTTON_LOCATOR will be used
    COLLAPSE_BUTTON_LOCATOR = None

    # (Default = True) True if element is a fixed navbar, False otherwise. If
    # set to False, click_page_link() and hover_over_page_link() will scroll
    # the target link into view before interacting with it
    FIXED = False


class NoYAMLCollapsibleNavFixed(NoYAMLCollapsibleNav):
    FIXED = True


