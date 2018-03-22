# Subclasses of BasePage with additional functions for convenience
from selenium.webdriver.common.action_chains import ActionChains


# TODO: Since a lot of these define interfaces, need to somehow document the stuff that subclasses will want to override

class WebPageObject(BasePage):
    """Page object prototype for web pages"""

    # File name of the page relative to config.SiteConfig.BASE_URL
    PAGE_FILENAME = None

    def get_page_title(self):
        """Get the title of the current page

        :return: Title of the current page
        """
        return driver.get_title()


class NavObject(BasePage):
    """Page object prototype for navbars"""

    # Maps link text to a tuple containing its locator and the page object class for the target page, modal, section, etc
    LINK_MAP = {}

    # Page Functions
    # --------------------------------

    def click_page_link(self, link_map_key):
        """Click one of the page links and return a page object class for the link target

        :param link_map_key: Key into LINK_MAP for the link to click on
        :return: Corresponding page object class for the link target
        """
        # TODO: raise exception?
        if link_map_key in self.LINK_MAP:
            link_tuple = self.LINK_MAP[link_map_key]
            self.find_element(link_tuple[0]).click()
            # Initialize the target page object and return it
            return link_tuple[1](self.driver)


    # TODO: extend LINK_MAP to have different page objects for hovering and clicking and return corresponding hover object?
    def hover_over_page_link(self, link_map_key):
        """Hover mouse over one of the page links

        :param link_map_key: Key into LINK_MAP for the link to hover mouse over
        """
        # TODO: raise exception?
        if link_map_key in self.LINK_MAP:
            link_tuple = self.LINK_MAP[link_map_key]
            link = self.find_element(link_tuple[0])
            action_chain = ActionChains(driver)
            action_chain.move_to_element(link).perform()


class FormObject(BasePage):
    """Page object prototype for navbars"""

    class Input(object):
        """Subclass used to contain name attributes and select/radio option lists for inputs

        :Example:

            SOME_INPUT = 'someInput'

            SOME_SELECT = 'someSelect'
            SOME_SELECT_OPTIONS = [
                    'vaule1',
                    'value2',
            ]
        """
        pass

    # TODO: fill_form()

    # TODO: submit_is_enabled()

    # TODO: click_submit()



