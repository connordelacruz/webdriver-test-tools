from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains

from webdriver_test_tools.pageobject import utils, BasePage, YAMLParsingPageObject
from webdriver_test_tools.webdriver import actions


# Link Page Objects

class NavLinkObject(BasePage):
    # TODO: doc and implement

    class ActionTypes:
        # TODO: doc
        PAGE = 'page'
        SECTION = 'section'
        MENU = 'menu'
        # Click/hover support for each type
        CLICK_ACTIONS = [
            PAGE, SECTION, MENU
        ]
        HOVER_ACTIONS = [
            MENU
        ]

    def __init__(self, driver, link_dict):
        # TODO: doc
        super().__init__(driver)
        # 'name' and 'link_locator' required, so assume that they're valid keys
        # and raise errors otherwise
        self.name = link_dict['name']
        self.locator = utils.yaml.to_locator(link_dict['link_locator'])
        # TODO: raise value errors if invalid
        self.click_action = link_dict.get('click', self.ActionTypes.PAGE)
        self.hover_action = link_dict.get('hover', None)
        # TODO: raise key error if click_action is page/section
        self.target = link_dict.get('target', None)
        # Parse menu if applicable
        if self.ActionTypes.MENU in [self.click_action, self.hover_action]:
            # TODO: self.menu = NavMenuObject(self.driver, link_dict['menu'])
            pass

    # WebElement retrieval

    def find_link_element(self):
        """Returns the ``WebElement`` object located by ``self.locator``

        Shorthand for ``self.find_element(self.locator)``

        :return: ``WebElement`` object for the link
        """
        return self.find_element(self.locator)

    # Actions

    def click_link(self):
        actions.scroll.to_and_click(self.driver, self.find_link_element(), False)
        # TODO: return something? (and doc)

    def hover_over_link(self):
        link_element = self.find_link_element()
        actions.scroll.into_view(self.driver, link_element, False)
        action_chain = ActionChains(self.driver)
        action_chain.move_to_element(link_element).perform()
        # TODO: return menu object? (and doc)


# Menu Page Objects

class NavMenuObject(BasePage):
    # TODO: doc and implement

    def __init__(self, driver, menu_dict):
        # TODO: doc
        super().__init__(driver)
        # 'menu_locator' is required, so assume it's a valid key and raise
        # errors otherwise
        self.locator = menu_dict['menu_locator']
        # TODO: link map
        self.links = {}
        for link_dict in menu_dict['links']:
            # TODO: except key error
            link_name = link_dict['name']
            # TODO: raise (yaml) value error if name not unique
            self.links[link_name] = NavLinkObject(self.driver, link_dict)

    # WebElement retrieval

    def find_menu_element(self):
        """Returns the ``WebElement`` object located by ``self.locator``

        Shorthand for ``self.find_element(self.locator)``

        :return: ``WebElement`` object for the menu
        """
        return self.find_element(self.locator)

    # Actions

    def click_link(self, link_name):
        # TODO: doc, return something, errors?
        self.links[link_name].click_link()

    def hover_over_link(self, link_name):
        # TODO: doc, return something, errors?
        self.links[link_name].hover_over_link()


# Navbar Page Objects

# TODO: YAML support, implement new objects, update docs
class NavObject(BasePage):
    """Page object prototype for navbars

    :var NavObject.LINK_MAP: Maps link text to a tuple containing its locator
        and the page object class for the target page, modal, section, etc (or
        None if need be). Override in subclasses
    :var NavObject.HOVER_MAP: Maps link text to a tuple containing its locator
        and the page object class for the menu, dropdown, etc that should
        appear on hover (or None if need be). Override in subclasses
    :var NavObject.FIXED: (Default = True) True if element is a fixed navbar,
        False otherwise. If set to False in a subclass,
        :meth:`click_page_link()` and :meth:`hover_over_page_link()` will
        scroll the target link into view before interacting with it
    """

    # Link maps
    LINK_MAP = {}
    HOVER_MAP = {}
    # Nav attributes
    FIXED = True

    def click_page_link(self, link_map_key):
        """Click one of the page links and return a page object class for the link
        target

        :param link_map_key: Key into :attr:`LINK_MAP` for the link to click on

        :return: Corresponding page object class for the link target (if applicable)
        """
        if link_map_key in self.LINK_MAP:
            link_tuple = self.LINK_MAP[link_map_key]
            link = self.find_element(link_tuple[0])
            if not self.FIXED:
                actions.scroll.into_view(self.driver, link)
            link.click()
            # Initialize the target page object and return it
            return None if link_tuple[1] is None else link_tuple[1](self.driver)

    def hover_over_page_link(self, link_map_key):
        """Hover mouse over one of the page links

        :param link_map_key: Key into :attr:`HOVER_MAP` for the link to hover mouse over

        :return: Corresponding page object class for the hover dropdown/container/etc
            (if applicable)
        """
        if link_map_key in self.HOVER_MAP:
            link_tuple = self.HOVER_MAP[link_map_key]
            link = self.find_element(link_tuple[0])
            if not self.FIXED:
                actions.scroll.into_view(self.driver, link)
            action_chain = ActionChains(self.driver)
            action_chain.move_to_element(link).perform()
            # Initialize the target page object and return it
            return None if link_tuple[1] is None else link_tuple[1](self.driver)


class CollapsibleNavObject(NavObject):
    """Subclass of :class:`NavObject` with additional methods for collapsible nav menus

    In addition to the variables for :class:`NavObject`, the following variables need to
    be defined for collapsible navs

    :var CollapsibleNavObject.EXPAND_BUTTON_LOCATOR: Locator for the button
        that expands the nav menu
    :var CollapsibleNavObject.COLLAPSE_BUTTON_LOCATOR: Locator for the button
        that expands the nav menu
    :var CollapsibleNavObject.MENU_CONTAINER_LOCATOR: Locator for the
        collapsing/expanding container of the navigation menu
    """

    EXPAND_BUTTON_LOCATOR = None
    COLLAPSE_BUTTON_LOCATOR = None
    MENU_CONTAINER_LOCATOR = None

    def is_expanded(self):
        """Check if the nav menu is expanded

        This method checks if the element located by :attr:`MENU_CONTAINER_LOCATOR`
        exists and is visible. This should be sufficient for many common implementations
        of collapsible navs, but can be overridden if this isn't a reliable detection
        method for an implementation

        :return: True if the nav menu is expanded, False if it's collapsed
        """
        try:
            expanded = self.find_element(self.MENU_CONTAINER_LOCATOR).is_displayed()
        except NoSuchElementException:
            expanded = False
        return expanded

    def click_expand_button(self):
        """Click the button to expand the nav menu"""
        button = self.find_element(self.EXPAND_BUTTON_LOCATOR)
        if not self.FIXED:
            actions.scroll.into_view(self.driver, button)
        button.click()

    def click_collapse_button(self):
        """Click the button to collapse the nav menu"""
        button = self.find_element(self.COLLAPSE_BUTTON_LOCATOR)
        if not self.FIXED:
            actions.scroll.into_view(self.driver, button)
        button.click()

