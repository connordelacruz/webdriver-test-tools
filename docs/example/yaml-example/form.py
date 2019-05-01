import os

from selenium.webdriver.common.by import By
from webdriver_test_tools.pageobject import *
from webdriver_test_tools.webdriver import actions, locate


class ExampleFormObject(prototypes.FormObject):
    """YAML FormObject example"""

    # Path to YAML file representing the object
    YAML_FILE = os.path.join(os.path.dirname(__file__), 'form.yml')

    # (Optional) Page object of the modal/webpage/etc that should appear on
    # successful form submission. If set to a subclass of BasePage, the
    # click_submit() method will return an instance of the page object
    SUBMIT_SUCCESS_CLASS = None
