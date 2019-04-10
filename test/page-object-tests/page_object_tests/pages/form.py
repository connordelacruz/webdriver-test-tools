import os

from selenium.webdriver.common.by import By
from webdriver_test_tools.pageobject import *
from webdriver_test_tools.webdriver import actions, locate


class TestFormObject(prototypes.FormObject):

    PAGE_FILENAME = 'form.html'

    class Locator:
        """WebDriver locator tuples for any elements that will need to be
        accessed by this page object.
        """
        pass

    # SET THE FOLLOWING ATTRIBUTES TO USE IN FormObject METHODS

    YAML_FILE = os.path.join(os.path.dirname(__file__), 'form.yml')
    # Locator for the form element
    # FORM_LOCATOR = None
    # Locator for the form submit button
    # SUBMIT_LOCATOR = None
    # (Optional) Page object of the modal/webpage/etc that should appear on
    # successful form submission. If set to a subclass of BasePage, the
    # click_submit() method will return an instance of the page object
    SUBMIT_SUCCESS_CLASS = None
