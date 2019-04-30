from selenium.webdriver.common.by import By
from webdriver_test_tools.pageobject import *
from webdriver_test_tools.webdriver import actions, locate


class ExampleModalObject(prototypes.ModalObject):
    """Non-YAML ModalObject example"""

    # REQUIRED: Locator for the modal element
    MODAL_LOCATOR = (By.ID, 'test-modal')
    # REQUIRED: Locator for the modal's close button
    CLOSE_LOCATOR = (By.CSS_SELECTOR, '#test-modal button.close')
    # (Optional) Page object of the contents of the modal body. If set to a
    # subclass of BasePage, the get_modal_body() method will return an instance
    # of the page object
    MODAL_BODY_CLASS = None
