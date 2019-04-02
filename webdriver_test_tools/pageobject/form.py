import inspect
import os
from selenium.webdriver.common.by import By
from webdriver_test_tools.pageobject import utils, BasePage
from webdriver_test_tools.webdriver import actions


class InputObject(BasePage):
    """Page object prototype for input elements"""

    class Type:
        """Set of supported input types"""
        # https://www.w3schools.com/html/html_form_input_types.asp
        # TODO: comment out unsupported?
        # Standard <input> tag types
        BUTTON = 'button'
        CHECKBOX = 'checkbox'
        COLOR = 'color'
        DATE = 'date'
        DATETIME_LOCAL = 'datetime-local'
        EMAIL = 'email'
        FILE = 'file'
        HIDDEN = 'hidden'
        IMAGE = 'image'
        MONTH = 'month'
        NUMBER = 'number'
        PASSWORD = 'password'
        RADIO = 'radio'
        RANGE = 'range'
        RESET = 'reset'
        SEARCH = 'search'
        SUBMIT = 'submit'
        TEL = 'tel'
        TEXT = 'text'
        TIME = 'time'
        URL = 'url'
        WEEK = 'week'
        # Non-<input> tag inputs
        SELECT = 'select'
        TEXTAREA = 'textarea'
        # TODO: group similar input types (text, selectable, etc) in arrays?
        # Attribute support based on input types
        SUPPORTS_OPTIONS = [
            SELECT,
            RADIO,
            CHECKBOX,
        ]
        SUPPORTS_MULTIPLE = [
            SELECT,
        ]


    # TODO: document params
    def __init__(self, driver, form_element, input_dict):
        super().__init__(driver)
        # TODO: may not be required after updating actions.form?
        self.form_element = form_element
        # 'name' is required, so assume that it's a valid key and raise errors
        # otherwise
        self.name = input_dict['name']
        # If 'input_locator' is specified, use that as the locator, otherwise
        # find using self.name
        if 'input_locator' in input_dict:
            self.locator = utils.yaml.to_locator(input_dict['input_locator'])
        else:
            self.locator = (By.NAME, self.name)
        # Get input type, default to 'text' if unspecified
        # TODO: validate type based on attributes in self.Type
        self.type = input_dict.get('type', self.Type.TEXT)
        # Assume input is required unless otherwise specified
        self.required = input_dict.get('required', True)
        # Retrieve list of options (for radios and selects)
        if self.type in self.Type.SUPPORTS_OPTIONS:
            self.options = input_dict.get('options', None)
        else:
            # Ensures options attribute is ignored for inputs that don't
            # support it
            self.options = None
        # (For select inputs) Assume only one option can be selected unless
        # otherwise specified
        if self.type in self.Type.SUPPORTS_MULTIPLE:
            self.multiple = input_dict.get('multiple', False)
        else:
            # Ensure multiple attribute is ignored for inputs that don't
            # support it
            self.multiple = None

    def set_value(self, value):
        """Set the value of the input

        :param value: The value to set it to
        """
        # TODO: document value format
        # TODO: validate value if self.options is not None
        # TODO: currently this only supports inputs with name attributes
        actions.fill_form_input(
            self.driver, self.form_element,
            self.name, value,
            input_type=self.type
        )

    def get_value(self):
        """Returns the current value of the input"""
        return actions.get_form_input_value(
            self.find_element(self.locator),
            input_type=self.type
        )


class FormObject(BasePage):
    """Page object prototype for forms

    :var FORM_LOCATOR: Locator for the form element. Override in subclasses
    :var SUBMIT_LOCATOR: Locator for the submit button. Override in subclasses
    :var SUBMIT_SUCCESS_CLASS: (Optional) Page object of modal/webpage/etc that
        should appear on successful form submission. If subclass set to a subclass of
        :class:`BasePage <webdriver_test_tools.pageobject.base.BasePage>`,
        :meth:`click_submit()` will return an instance of this object.
    """

    # Locators
    FORM_LOCATOR = None
    SUBMIT_LOCATOR = None
    # Optional page object to return on click_submit()
    SUBMIT_SUCCESS_CLASS = None
    # Optional attribute with path to YAML file (parsed on __init__)
    # TODO: Update docstring
    YAML_FILE = None

    # TODO: deprecate Input class?
    class Input:
        """Subclass used to contain name attributes and select/radio option lists for
        inputs

        :Example:

            .. code-block:: python

                SOME_INPUT = 'someInput'

                SOME_SELECT = 'someSelect'
                SOME_SELECT_OPTIONS = [
                        'vaule1',
                        'value2',
                ]

        """
        pass

    def __init__(self, driver):
        super().__init__(driver)
        if self.YAML_FILE:
            self.parse_yaml(self.YAML_FILE)

    def parse_yaml(self, file_path):
        # TODO: doc and implement
        parsed_yaml = utils.yaml.parse_yaml_file(file_path)['form']
        # Initialize locators
        # TODO: raise exception w/ helpful message if any required keys are missing
        self.FORM_LOCATOR = utils.yaml.to_locator(parsed_yaml['form_locator'])
        self.SUBMIT_LOCATOR = utils.yaml.to_locator(parsed_yaml['submit_locator'])
        # TODO: document attribute
        self.form_element = self.find_element(self.FORM_LOCATOR)
        # Initialize inputs
        self.inputs = {}
        for input_dict in parsed_yaml['inputs']:
            # TODO: throw exception if name isn't set (or validate during parse_yaml_file()?)
            # TODO: use !!python/object instead (see https://pyyaml.org/wiki/PyYAMLDocumentation)?
            self.inputs[input_dict['name']] = InputObject(self.driver, self.form_element, input_dict)

    # TODO: deprecate input_map
    def fill_form(self, input_map):
        """Fill the form element inputs

        :param input_map: Dictionary mapping input names to the values to set them to.
            See :func:`webdriver_test_tools.webdriver.actions.form.fill_form_input`
            for values to use for different input types
        """
        form = self.find_element(self.FORM_LOCATOR)
        actions.form.fill_form_inputs(self.driver, form, input_map)

    def fill_inputs(self, **kwargs):
        # TODO: doc
        for name, value in kwargs.items():
            # TODO: handle invalid names
            self.inputs['name'].set_value(value)

    def submit_is_enabled(self):
        """Short hand function for checking if the submit button is enabled. Useful
        for forms with JavaScript input validation

        :return: True if submit is enabled, False if it's disabled
        """
        return self.find_element(self.SUBMIT_LOCATOR).is_enabled()

    def click_submit(self):
        """Shorthand function for scrolling to the submit button and clicking it.

        If :attr:`self.SUBMIT_SUCCESS_CLASS <SUBMIT_SUCCESS_CLASS>` is set to a
        subclass of :class:`BasePage
        <webdriver_test_tools.pageobject.base.BasePage>`, an instance of that
        object will be returned
        """
        submit_button = self.find_element(self.SUBMIT_LOCATOR)
        actions.scroll.to_and_click(self.driver, submit_button, False)
        if inspect.isclass(self.SUBMIT_SUCCESS_CLASS) and issubclass(self.SUBMIT_SUCCESS_CLASS, BasePage):
            return self.SUBMIT_SUCCESS_CLASS(self.driver)

