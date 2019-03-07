from selenium.common.exceptions import NoSuchElementException

from webdriver_test_tools.pageobject import BasePage
from webdriver_test_tools.webdriver import actions


class ModalObject(BasePage):
    """Page object prototype for modals

    :var MODAL_LOCATOR: Locator for the modal element. Override in subclasses
    :var CLOSE_LOCATOR: Locator for the close button. Override in subclasses
    :var MODAL_BODY_CLASS: (Optional) Page object for the contents of the modal body.
        If set to a subclass of
        :class:`BasePage <webdriver_test_tools.pageobject.base.BasePage>`,
        :meth:`get_modal_body()` will return an instance of this object.
    """
    # Locators
    MODAL_LOCATOR = None
    CLOSE_LOCATOR = None
    # Optional page object for the modal body content
    MODAL_BODY_CLASS = None

    def is_displayed(self):
        """Check if the modal is displayed

        This method checks if the element located by :attr:`MODAL_LOCATOR`
        exists and is visible. This should be sufficient for many common implementations
        of modals, but can be overridden if this isn't a reliable detection
        method for an implementation

        :return: True if the modal is displayed, False otherwise
        """
        try:
            displayed = self.find_element(self.MODAL_LOCATOR).is_displayed()
        except NoSuchElementException:
            displayed = False
        return displayed

    def click_close_button(self):
        """Click the modal close button"""
        actions.scroll.to_and_click(self.driver, self.find_element(self.CLOSE_LOCATOR))

    def get_modal_body(self):
        """If :attr:`self.MODAL_BODY_CLASS <MODAL_BODY_CLASS>` is set to a subclass of
        :class:`BasePage <webdriver_test_tools.pageobject.base.BasePage>`,
        returns an instance of that object. Otherwise, returns None
        """
        return self.MODAL_BODY_CLASS(self.driver) if issubclass(self.MODAL_BODY_CLASS, BasePage) else None

