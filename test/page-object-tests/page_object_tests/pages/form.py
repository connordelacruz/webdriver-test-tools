import os

from selenium.webdriver.common.by import By
from webdriver_test_tools.pageobject import *
from webdriver_test_tools.webdriver import actions, locate


class YAMLForm(prototypes.FormObject):

    PAGE_FILENAME = 'form.html'

    YAML_FILE = os.path.join(os.path.dirname(__file__), 'form.yml')
    # (Optional) Page object of the modal/webpage/etc that should appear on
    # successful form submission. If set to a subclass of BasePage, the
    # click_submit() method will return an instance of the page object
    SUBMIT_SUCCESS_CLASS = None


class NoYAMLForm(prototypes.FormObject):

    PAGE_FILENAME = 'form.html'

    # REQUIRED: Locator for the form element
    FORM_LOCATOR = (By.ID, 'test-form')
    # REQUIRED: Locator for the form submit button
    SUBMIT_LOCATOR = (By.CSS_SELECTOR, 'button[type="submit"]')

    # REQUIRED: List of input dictionaries. These will be used to initialize
    # InputObjects at run time.
    INPUT_DICTS = [
        {
            'name': 'optText'
        },
        {
            'name': 'optRadio',
            'type': 'radio',
            'options': ['1', '2']
        },
        {
            'name': 'optCheckbox',
            'type': 'checkbox'
        },
        {
            'name': 'optCheckboxGroup[]',
            'type': 'checkbox',
            'multiple': True,
            'options': ['1', '2', '3']
        },
        {
            'name': 'optSelect',
            'type': 'select',
            'options': ['1', '2']
        },
        {
            'name': 'optMultipleSelect',
            'type': 'select',
            'multiple': True,
            'options': ['1', '2', '3']
        }
    ]

    # (Optional) Page object of the modal/webpage/etc that should appear on
    # successful form submission. If set to a subclass of BasePage, the
    # click_submit() method will return an instance of the page object
    SUBMIT_SUCCESS_CLASS = None
