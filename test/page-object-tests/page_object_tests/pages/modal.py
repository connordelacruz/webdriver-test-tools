import os

from selenium.webdriver.common.by import By
from webdriver_test_tools.pageobject import *
from webdriver_test_tools.webdriver import actions, locate


# Modal Classes

class YAMLModal(prototypes.ModalObject):

    # Path to YAML file representing the modal object
    YAML_FILE = os.path.join(os.path.dirname(__file__), 'modal.yml')

    # (Optional) Page object of the contents of the modal body. If set to a
    # subclass of BasePage, the get_modal_body() method will return an instance
    # of the page object
    MODAL_BODY_CLASS = None


class NoYAMLModal(prototypes.ModalObject):

    # REQUIRED: Locator for the modal element
    MODAL_LOCATOR = (By.ID, 'test-modal')
    # REQUIRED: Locator for the modal's close button
    CLOSE_LOCATOR = (By.CSS_SELECTOR, '#test-modal button.close')
    # (Optional) Page object of the contents of the modal body. If set to a
    # subclass of BasePage, the get_modal_body() method will return an instance
    # of the page object
    MODAL_BODY_CLASS = None


# Page w/ modal open button

class ModalPage(BasePage):

    PAGE_FILENAME = 'modal.html'

    class Locator:
        OPEN_MODAL_BUTTON = (By.ID, 'open-modal-button')

    def __init__(self, driver, modal_class):
        """Extended constructor. Takes additional parameter modal_class, which
        sets the return type of click_open_modal_button()
        """
        super().__init__(driver)
        self.modal_class = modal_class

    def click_open_modal_button(self):
        """Click modal open button

        :return: Instance of self.modal_class
        """
        actions.scroll.to_and_click(self.driver, self.find_element(self.Locator.OPEN_MODAL_BUTTON))
        return self.modal_class(self.driver)

