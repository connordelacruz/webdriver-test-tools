from webdriver_test_tools.classes.base_page import BasePage
from webdriver_test_tools.webdriver import actions
from selenium.webdriver.common.by import By


class TemplatePage(BasePage):

    class Locator(object):
        """WebDriver locator tuples for any elements that will need to be accessed by
        this page object.

        :Example:

            SOME_ELEMENT = (By.ID, 'some-element')
        """
        pass


    # Page Functions
    # --------------------------------


