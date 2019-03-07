from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains

from webdriver_test_tools.pageobject import BasePage
from webdriver_test_tools.webdriver import actions


class NavObject(BasePage):
    """Page object prototype for navbars

    :var LINK_MAP:  Maps link text to a tuple containing its locator and the page object
        class for the target page, modal, section, etc (or None if need be).
        Override in subclasses
    :var HOVER_MAP: Maps link text to a tuple containing its locator and the page
        object class for the menu, dropdown, etc that should appear on hover (or None
        if need be). Override in subclasses
    :var fixed: (Default = True) True if element is a fixed navbar, False otherwise. If
        set to False in a subclass, :meth:`click_page_link()` and
        :meth:`hover_over_page_link()` will scroll the target link into view before
        interacting with it
    """

    # Link maps
    LINK_MAP = {}
    HOVER_MAP = {}
    # Nav attributes
    fixed = True

    def click_page_link(self, link_map_key):
        """Click one of the page links and return a page object class for the link
        target

        :param link_map_key: Key into :attr:`LINK_MAP` for the link to click on

        :return: Corresponding page object class for the link target (if applicable)
        """
        if link_map_key in self.LINK_MAP:
            link_tuple = self.LINK_MAP[link_map_key]
            link = self.find_element(link_tuple[0])
            if not self.fixed:
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
            if not self.fixed:
                actions.scroll.into_view(self.driver, link)
            action_chain = ActionChains(self.driver)
            action_chain.move_to_element(link).perform()
            # Initialize the target page object and return it
            return None if link_tuple[1] is None else link_tuple[1](self.driver)


class CollapsibleNavObject(NavObject):
    """Subclass of :class:`NavObject` with additional methods for collapsible nav menus

    In addition to the variables for :class:`NavObject`, the following variables need to
    be defined for collapsible navs

    :var EXPAND_BUTTON_LOCATOR: Locator for the button that expands the nav menu
    :var COLLAPSE_BUTTON_LOCATOR: Locator for the button that expands the nav menu
    :var MENU_CONTAINER_LOCATOR: Locator for the collapsing/expanding container of the
        navigation menu
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
        if not self.fixed:
            actions.scroll.into_view(self.driver, button)
        button.click()

    def click_collapse_button(self):
        """Click the button to collapse the nav menu"""
        button = self.find_element(self.COLLAPSE_BUTTON_LOCATOR)
        if not self.fixed:
            actions.scroll.into_view(self.driver, button)
        button.click()

