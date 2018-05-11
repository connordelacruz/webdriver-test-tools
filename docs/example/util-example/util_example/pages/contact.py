from webdriver_test_tools.pageobject import BasePage
from webdriver_test_tools.pageobject.prototypes import FormObject, ModalObject
from webdriver_test_tools.webdriver import actions, locate
from selenium.webdriver.common.by import By


class ContactPage(FormObject):
    # Relative to SiteConfig.BASE_URL
    PAGE_FILENAME = 'contact.html'

    class Locator:
        CONTACT_FORM = (By.ID, 'contact-form')
        SUBMIT = (By.CSS_SELECTOR, 'button[type="submit"]')

    # Attributes used by FormObject methods
    FORM_LOCATOR = Locator.CONTACT_FORM
    SUBMIT_LOCATOR = Locator.SUBMIT
    SUBMIT_SUCCESS_CLASS = SuccessModal

    class Input:
        """Constants for input names"""
        FIRST_NAME = 'firstname'
        LAST_NAME = 'lastname'
        EMAIL = 'email'
        MESSAGE = 'message'


class SuccessModal(ModalObject):

    class Locator:
        SUCCESS_MODAL = (By.ID, 'success-modal')
        CLOSE_BUTTON = (By.ID, 'close')

    # Attributes used by ModalObject methods
    MODAL_LOCATOR = Locator.SUCCESS_MODAL
    CLOSE_LOCATOR = Locator.CLOSE_BUTTON

