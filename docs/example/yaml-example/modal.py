import os

from selenium.webdriver.common.by import By
from webdriver_test_tools.pageobject import *
from webdriver_test_tools.webdriver import actions, locate


class ExampleModalObject(prototypes.ModalObject):
    """YAML ModalObject example"""

    # Path to YAML file representing the object
    YAML_FILE = os.path.join(os.path.dirname(__file__), 'modal.yml')

    # (Optional) Page object of the contents of the modal body. If set to a
    # subclass of BasePage, the get_modal_body() method will return an instance
    # of the page object
    MODAL_BODY_CLASS = None
