from selenium.webdriver.common.by import By
from webdriver_test_tools.pageobject import *
from webdriver_test_tools.webdriver import actions, locate

from page_object_tests.config import SiteConfig


class NoYAMLNavObject(prototypes.NavObject):

    class Locator:
        """WebDriver locator tuples for any elements that will need to be
        accessed by this page object.
        """
        pass

    # Used for internal methods (do not modify)
    SITE_CONFIG = SiteConfig

    # SET THE FOLLOWING ATTRIBUTES TO USE IN NavObject METHODS

    # REQUIRED: List of link dictionaries. These will be used to initialize
    # NavLinkObject instances at runtime.
    # Dictionaries use same keys as YAML links. For syntax, see:
    # https://connordelacruz.com/webdriver-test-tools/yaml.html#yaml-links

    # TODO: update to support new syntax
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
            'click': 'none',
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

    # UNCOMMENT BELOW TO OVERRIDE NavObject DEFAULTS

    # (Default = True) True if element is a fixed navbar, False otherwise. If
    # set to False, click_page_link() and hover_over_page_link() will scroll
    # the target link into view before interacting with it
    FIXED = False


class NoYAMLCollapsibleNavObject(prototypes.NavObject):

    class Locator:
        """WebDriver locator tuples for any elements that will need to be
        accessed by this page object.
        """
        pass

    # Used for internal methods (do not modify)
    SITE_CONFIG = SiteConfig

    # SET THE FOLLOWING ATTRIBUTES TO USE IN NavObject METHODS

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

    # UNCOMMENT BELOW TO OVERRIDE NavObject DEFAULTS

    # (Default = True) True if element is a fixed navbar, False otherwise. If
    # set to False, click_page_link() and hover_over_page_link() will scroll
    # the target link into view before interacting with it
    FIXED = False

