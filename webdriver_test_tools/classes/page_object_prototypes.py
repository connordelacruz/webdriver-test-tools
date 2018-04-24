"""Subclasses of BasePage with additional functions for convenience.

These classes define common operations and attributes for various common components.
These can be subclassed in test projects if useful.
"""

from selenium.webdriver.common.action_chains import ActionChains
from webdriver_test_tools.classes.base_page import BasePage
from webdriver_test_tools.webdriver import actions
from webdriver_test_tools import test


class WebPageObject(BasePage):
    """Page object prototype for web pages

    :var PAGE_FILENAME: File name of the page relative to config.SiteConfig.BASE_URL
    """

    PAGE_FILENAME = None

    def get_page_title(self):
        """Get the title of the current page

        :return: Title of the current page
        """
        return driver.get_title()


class NavObject(BasePage):
    """Page object prototype for navbars

    :var LINK_MAP:  Maps link text to a tuple containing its locator and the page object
        class for the target page, modal, section, etc (or None if need be).
        Override in subclasses
    :var HOVER_MAP: Maps link text to a tuple containing its locator and the page
        object class for the menu, dropdown, etc that should appear on hover (or None
        if need be). Override in subclasses
    :var fixed: (Default = True) True if element is a fixed navbar, False otherwise. If
        set to False in a subclass, click_page_link() and hover_over_page_link() will
        scroll the target link into view before interacting with it
    """

    # Link maps
    LINK_MAP = {}
    HOVER_MAP = {}
    # Nav attributes
    fixed = True

    def click_page_link(self, link_map_key):
        """Click one of the page links and return a page object class for the link
        target

        :param link_map_key: Key into LINK_MAP for the link to click on

        :return: Corresponding page object class for the link target (if applicable)
        """
        # TODO: raise exception?
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

        :param link_map_key: Key into HOVER_MAP for the link to hover mouse over

        :return: Corresponding page object class for the hover dropdown/container/etc
            (if applicable)
        """
        # TODO: raise exception?
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
    """Subclass of NavObject with additional methods for collapsible nav menus

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
        driver = self.driver
        expanded = test.element_exists(driver, self.MENU_CONTAINER_LOCATOR) and self.find_element(self.MENU_CONTAINER_LOCATOR).is_displayed()
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


class FormObject(BasePage):
    """Page object prototype for navbars

    :var FORM_LOCATOR: Locator for the form element. Override in subclasses
    :var SUBMIT_LOCATOR: Locator for the submit button. Override in subclasses
    :var SUBMIT_SUCCESS_CLASS: (Optional) Page object of modal/webpage/etc that
        should appear on successful form submission. If subclass set to a subclass of
        BasePage, click_submit() will return an instance of this object.
    """

    # Locators
    FORM_LOCATOR = None
    SUBMIT_LOCATOR = None
    # Optional page object to return on click_submit()
    SUBMIT_SUCCESS_CLASS = None

    class Input(object):
        """Subclass used to contain name attributes and select/radio option lists for
        inputs

        :Example:

            .. code:: python

                SOME_INPUT = 'someInput'

                SOME_SELECT = 'someSelect'
                SOME_SELECT_OPTIONS = [
                        'vaule1',
                        'value2',
                ]

        """
        pass

    def fill_form(self, input_map):
        """Fill the form element inputs

        :param input_map: Dictionary mapping input names to the values to set them to.
            See webdriver_test_tools.webdriver.actions.form.fill_form_input for values
            to use for different input types
        """
        form = self.find_element(self.FORM_LOCATOR)
        actions.form.fill_form_inputs(self.driver, form, input_map)

    def submit_is_enabled(self):
        """Short hand function for checking if the submit button is enabled. Useful
        for forms with JavaScript input validation

        :return: True if submit is enabled, False if it's disabled
        """
        return self.find_element(self.SUBMIT_LOCATOR).is_enabled()

    def click_submit(self):
        """Shorthand function for scrolling to the submit button and clicking it.

        If self.SUBMIT_SUCCESS_CLASS is set to a subclass of BasePage, an instance of
        that object will be returned
        """
        submit_button = self.find_element(self.SUBMIT_LOCATOR)
        actions.scroll.to_and_click(self.driver, submit_button, False)
        if issubclass(self.SUBMIT_SUCCESS_CLASS, BasePage):
            return self.SUBMIT_SUCCESS_CLASS(self.driver)



