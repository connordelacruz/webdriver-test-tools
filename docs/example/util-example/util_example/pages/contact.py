import os

from selenium.webdriver.common.by import By
from webdriver_test_tools.pageobject import *
from webdriver_test_tools.webdriver import actions, locate


class ContactPage(prototypes.FormObject):
    # Path to YAML file representing the form object
    YAML_FILE = os.path.join(os.path.dirname(__file__), 'contact.yml')

    # Relative to SiteConfig.BASE_URL
    PAGE_FILENAME = 'contact.html'

    # Page object class to return on click_submit()
    SUBMIT_SUCCESS_CLASS = SuccessModal


class SuccessModal(prototypes.ModalObject):
    # Path to YAML file representing the modal object
    YAML_FILE = os.path.join(os.path.dirname(__file__), 'success_modal.yml')

