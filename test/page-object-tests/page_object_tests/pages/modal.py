import os

from selenium.webdriver.common.by import By
from webdriver_test_tools.pageobject import *
from webdriver_test_tools.webdriver import actions, locate


class ModalPage(BasePage):

    PAGE_FILENAME = 'modal.html'

    class Locator:
        OPEN_MODAL_BUTTON = (By.ID, 'open-modal-button')

    def click_open_modal_button(self):
        actions.scroll.to_and_click(self.driver, self.find_element(self.Locator.OPEN_MODAL_BUTTON))
        return TestModalObject(self.driver)


class TestModalObject(prototypes.ModalObject):

    class Locator:
        """WebDriver locator tuples for any elements that will need to be
        accessed by this page object.
        """
        pass

    # Path to YAML file representing the modal object
    YAML_FILE = os.path.join(os.path.dirname(__file__), 'modal.yml')

    # SET THE FOLLOWING ATTRIBUTES TO USE IN ModalObject METHODS

    # (Optional) Page object of the contents of the modal body. If set to a
    # subclass of BasePage, the get_modal_body() method will return an instance
    # of the page object
    MODAL_BODY_CLASS = None
