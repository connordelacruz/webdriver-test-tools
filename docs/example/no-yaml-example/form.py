from selenium.webdriver.common.by import By
from webdriver_test_tools.pageobject import *
from webdriver_test_tools.webdriver import actions, locate


class ExampleForm(prototypes.FormObject):
    """Non-YAML FormObject example"""

    # REQUIRED: Locator for the form element
    FORM_LOCATOR = (By.ID, 'example-form-id')
    # REQUIRED: Locator for the form submit button
    SUBMIT_LOCATOR = (By.CSS_SELECTOR, '#example-form-id button[type="submit"]')

    # Inputs are specified here:
    INPUT_DICTS = [
        # Basic syntax:
        {
            'name': 'email',
            'type': 'email'
        },
        # 'type' defaults to 'text' if not specified:
        {'name': 'text_input'},
        # Inputs are assumed to be required by default, use 'required' to
        # specify otherwise:
        {
            'name': 'optional_input',
            'required': False
        },
        # For input elements with no name attribute, the 'input_locator' key is
        # used to locate the element (though the 'name' key is still required
        # for identification):
        {
            'name': 'unique_identifier',
            'input_locator': (By.CLASS_NAME, 'input-with-no-name-attribute')
        },
        # Selects and radios take a list of options:
        {
            'name': 'select_example',
            'type': 'select',
            'options': [
                'option1',
                'option2',
                'option3',
                'option4',
            ]
        },
        # 'options' can bet a dictionary too. Only the keys are used, so the
        # values can be set to anything:
        {
            'name': 'radio_example',
            'type': 'radio',
            'options': {
                # NOTE: numeric options keys/list entries should be in quotes
                '001': 'Helpful label',
                '002': 'Another helpful label',
                '003': 'An even more helpful label',
            }
        },
        # Supports select elements with the 'multiple' attribute:
        {
            'name': 'multiple_select_example',
            'type': 'select',
            'multiple': True,
            'options': [
                'option1',
                'option2',
                'option3',
            ]
        },
        # Checkbox groups can accept a list of options too:
        {
            'name': 'checkboxes[]',
            'type': 'checkbox',
            # NOTE: set 'multiple' to True when multiple checkboxes have the
            # same name and different values
            'multiple': True,
            'options': [
                'box0',
                'box1',
                'box2',
            ]
        },
    ]

    # (Optional) Page object of the modal/webpage/etc that should appear on
    # successful form submission. If set to a subclass of BasePage, the
    # click_submit() method will return an instance of the page object
    SUBMIT_SUCCESS_CLASS = None

