from selenium.webdriver.common.by import By
from webdriver_test_tools.pageobject import *
from webdriver_test_tools.webdriver import actions, locate


class NoYAMLModalPage(BasePage):

    PAGE_FILENAME = 'modal.html'

    class Locator:
        OPEN_MODAL_BUTTON = (By.ID, 'open-modal-button')

    def click_open_modal_button(self):
        actions.scroll.to_and_click(self.driver, self.find_element(self.Locator.OPEN_MODAL_BUTTON))
        return NoYAMLModalObject(self.driver)


class NoYAMLModalObject(prototypes.ModalObject):

    class Locator:
        """WebDriver locator tuples for any elements that will need to be
        accessed by this page object.
        """
        pass

    # SET THE FOLLOWING ATTRIBUTES TO USE IN ModalObject METHODS

    # REQUIRED: Locator for the modal element
    MODAL_LOCATOR = (By.ID, 'test-modal')
    # REQUIRED: Locator for the modal's close button
    CLOSE_LOCATOR = (By.CSS_SELECTOR, '#test-modal button.close')
    # (Optional) Page object of the contents of the modal body. If set to a
    # subclass of BasePage, the get_modal_body() method will return an instance
    # of the page object
    MODAL_BODY_CLASS = None
