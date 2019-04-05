import inspect
import os
import warnings

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from webdriver_test_tools.pageobject import utils, BasePage
from webdriver_test_tools.webdriver import actions


# Input Page Objects

class InputObject(BasePage):
    """Page object prototype for input elements"""

    class Type:
        """Set of supported input types"""
        # https://www.w3schools.com/html/html_form_input_types.asp
        # Standard <input> tag types
        CHECKBOX = 'checkbox'
        EMAIL = 'email'
        FILE = 'file'
        NUMBER = 'number'
        PASSWORD = 'password'
        RADIO = 'radio'
        SEARCH = 'search'
        TEXT = 'text'
        URL = 'url'
        # TODO: Uncomment as support is added/verified
        # BUTTON = 'button'
        # COLOR = 'color'
        # DATE = 'date'
        # DATETIME_LOCAL = 'datetime-local'
        # HIDDEN = 'hidden'
        # IMAGE = 'image'
        # MONTH = 'month'
        # RANGE = 'range'
        # RESET = 'reset'
        # SUBMIT = 'submit'
        # TEL = 'tel'
        # TIME = 'time'
        # WEEK = 'week'
        # Non-<input> tag inputs
        SELECT = 'select'
        TEXTAREA = 'textarea'
        # Attribute support based on input types
        SUPPORTS_OPTIONS = [
            SELECT,
            RADIO,
            CHECKBOX,
        ]
        SUPPORTS_MULTIPLE = [
            SELECT,
            CHECKBOX,
        ]


    # TODO: document params
    def __init__(self, driver, input_dict):
        super().__init__(driver)
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
        # Determine the getter/setter methods based on type
        # Defaults to text input getter/setter methods
        # TODO: move getter/setter methods to strategry classes?
        if self.type == self.Type.RADIO:
            self._set_value = self._set_radio_value
            self._get_value = self._get_radio_value
        elif self.type == self.Type.CHECKBOX:
            if self.multiple:
                self._set_value = self._set_multiple_checkbox_values
                self._get_value = self._get_multiple_checkbox_values
            else:
                self._set_value = self._set_checkbox_value
                self._get_value = self._get_checkbox_value
        elif self.type == self.Type.SELECT:
            if self.multiple:
                self._set_value = self._set_multiple_select_values
                self._get_value = self._get_multiple_select_values
            else:
                self._set_value = self._set_select_value
                self._get_value = self._get_select_value

    # WebElement Retrieval methods

    def find_input_element(self):
        """Returns the ``WebElement`` object located by ``self.locator``

        Shorthand for ``self.find_element(self.locator)``

        :return: ``WebElement`` object for the input
        """
        return self.find_element(self.locator)

    def find_input_elements(self):
        """Returns the list of ``WebElement`` objects located by
        ``self.locator``. Used for input types that can have multiple elements
        corresponding to it (e.g. radios)

        Shorthand for ``self.find_elements(self.locator)``

        :return: List of ``WebElement`` objects for the inputs
        """
        return self.find_elements(self.locator)

    # Input Setter Methods

    def _set_radio_value(self, value):
        """Select the radio input located by ``self.locator`` with the
        specified ``value`` attribute

        :param value: The ``value`` attribute of the radio element to select
        """
        # Filter radio elements to the one that matches value
        radio_element = [
            element for element in self.find_input_elements()
            if element.get_attribute('value') == value
        ][0]
        actions.scroll.to_and_click(self.driver, radio_element, False)

    def _set_checkbox_value(self, value):
        """Set the checked state of the checkbox input

        :param value: True to check the box, False to uncheck it. This function
            will do nothing if the checkbox already matches the desired value
        """
        checkbox_element = self.find_input_element()
        # Return if value is already set correctly
        if checkbox_element.is_selected() == value:
            return
        actions.form.toggle_checkbox(self.driver, checkbox_element)

    def _set_multiple_checkbox_values(self, values):
        """Check/uncheck one or more checkboxes in a checkbox group

        :param values: Dictionary mapping checkbox input's ``value`` attribute
            to the desired checked state (True = check, False = uncheck).
            Checkboxes already in the desired state won't be modified
        """
        checkbox_elements = [
            element for element in self.find_input_elements()
            if element.get_attribute('value') in values
            and element.is_selected != values[element.get_attribute('value')]
        ]
        for checkbox_element in checkbox_elements:
            actions.form.toggle_checkbox(self.driver, checkbox_element)

    def _set_text_value(self, value, clear_current_value=False):
        """Set the value of the text input

        Used for text inputs and other input types that are functionally
        similar (e.g. textarea, email, etc)

        :param value: The string to set the input value to. Uses
            ``WebElement.send_keys()`` method to set
        :param clear_current_value: (Default = False) If True, clear any
            existing value in the input before entering the new one
        """
        input_element = self.find_input_element()
        if clear_current_value:
            input_element.clear()
        input_element.send_keys(value)

    def _set_select_value(self, value):
        """Select an option in the select element

        :param value: The ``value`` attribute of the option to select
        """
        # TODO: validate value using self.options
        select = Select(self.find_input_element())
        select.select_by_value(value)

    def _set_multiple_select_values(self, values, clear_current_value=False):
        """Select one or more options in a multiple select element

        :param values: List of ``value`` attributes for the options to select
            (or a single ``value`` attribute if only one needs to be selected)
        :param clear_current_value: (Default = False) if True, deselect any
            currently selected options before selecting the new ones
        """
        select = Select(self.find_input_element())
        if clear_current_value:
            select.deselect_all()
        # If values is just a single item, make it a list with just itself to
        # avoid any iteration issues (e.g. if it's a string)
        if not isinstance(values, (list, dict)):
            values = [values]
        # TODO: validate value using self.options
        for value in values:
            select.select_by_value(value)

    # Internal attribute for setter method. Gets set after determining input
    # type in __init__() (defaults to text)
    _set_value = _set_text_value

    # TODO: document input type value formats
    def set_value(self, value, **kwargs):
        """Set the value of the input

        :param value: The value to set it to

        Additionally accepts keyword arguments based on the type of input this
        ``InputObject`` represents. See the above ``_set`` methods for
        type-specific optional arguments
        """
        self._set_value(value, **kwargs)

    # Input Getter Methods

    def _get_radio_value(self):
        """Returns the ``value`` attribute of the selected radio input

        :return: The ``value`` attribute of the selected radio input or
            ``None`` if all radios located with ``self.locator`` are deselected
        """
        selected_radio_list = [
            element for element in self.find_input_elements()
            if element.is_selected()
        ]
        # If none of the radios are selected, return None
        return selected_radio_list[0].get_attribute('value') if selected_radio_list else None

    def _get_checkbox_value(self):
        """Returns the checked state of the checkbox input

        :return: True if the checkbox is checked, False if it's unchecked
        """
        return self.find_input_element().is_selected()

    def _get_multiple_checkbox_values(self):
        """Returns a dictionary mapping ``value`` attributes of each checkbox
        to True if checked, False if unchecked

        :return: Dictionary mapping ``value`` attributes of each checkbox to
            True if checked, False if unchecked
        """
        return {
            checkbox_element.get_attribute('value'): checkbox_element.is_selected()
            for checkbox_element in self.find_input_elements()
        }

    def _get_text_value(self):
        """Returns the value of the text input

        :return: The value of the text input
        """
        return self.find_input_element().get_attribute('value')

    def _get_select_value(self):
        """Returns the ``value`` attribute of the selected option element

        :return: The ``value`` attribute of the selected option element or
            ``None`` if nothing is selected
        """
        select = Select(self.find_input_element())
        try:
            value = select.first_selected_option.get_attribute('value')
        except NoSuchElementException:
            value = None
        return value

    def _get_multiple_select_values(self):
        """Returns a list of ``value`` attributes of the selected option
        elements

        :return: List of ``value`` attributes of the selected option elements
            or an empty list if nothing is selected
        """
        select = Select(self.find_input_element())
        return [option.get_attribute('value') for option in select.all_selected_options]

    # Internal attribute for getter method. Gets set after determining input
    # type in __init__() (defaults to text)
    _get_value = _get_text_value

    def get_value(self):
        """Returns the current value of the input"""
        return self._get_value()


# Form Page Objects

# TODO: update docstring to reflect yaml stuff
class FormObject(BasePage):
    """Page object prototype for forms

    :var FORM_LOCATOR: Locator for the form element. Override in subclasses
    :var SUBMIT_LOCATOR: Locator for the submit button. Override in subclasses
    :var SUBMIT_SUCCESS_CLASS: (Optional) Page object of modal/webpage/etc that
        should appear on successful form submission. If subclass set to a subclass of
        :class:`BasePage <webdriver_test_tools.pageobject.base.BasePage>`,
        :meth:`click_submit()` will return an instance of this object.
    :var YAML_FILENAME: (Optional) Path to a YAML file representing the form
        object. This will be used to determine ``FORM_LOCATOR`` and
        ``SUBMIT_LOCATOR`` and create :class:`InputObject
        <webdriver_test_tools.pageobject.form.InputObject>` instances for each
        input
    """

    # Locators
    FORM_LOCATOR = None
    SUBMIT_LOCATOR = None
    # Optional page object to return on click_submit()
    SUBMIT_SUCCESS_CLASS = None
    # Optional attribute with path to YAML file (parsed on __init__)
    YAML_FILE = None
    # TODO: document form_element and inputs attributes, initialize to None/{}

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

    # TODO: link yaml syntax doc
    def parse_yaml(self, file_path):
        """Parse a YAML representation of the form object and set attributes
        accordingly

        :param file_path: Full path to the YAML file
        """
        try:
            parsed_yaml = utils.yaml.parse_yaml_file(file_path)['form']
        except KeyError as e:
            raise utils.yaml.YAMLKeyError(
                "Missing top level 'form' key in YAML"
            )
        # Initialize locators
        try:
            self.FORM_LOCATOR = utils.yaml.to_locator(parsed_yaml['form_locator'])
            self.SUBMIT_LOCATOR = utils.yaml.to_locator(parsed_yaml['submit_locator'])
        except KeyError as e:
            raise utils.yaml.YAMLKeyError(
                'Missing required {} key in form YAML'.format(e)
            )
        # Initialize inputs
        self.inputs = {}
        for input_dict in parsed_yaml['inputs']:
            try:
                # TODO: Use different attribute as key so name can change without affecting code?
                # TODO: Verify unique names
                self.inputs[input_dict['name']] = InputObject(self.driver, input_dict)
            except KeyError as e:
                error_msg = "Missing required 'name' key in input YAML (input: {})".format(str(input_dict))
                raise utils.yaml.YAMLKeyError(error_msg)

    # TODO: deprecate old fill_form workflow
    def fill_form(self, input_map):
        """
        .. deprecated:: 2.7.0
           Use :meth:`fill_inputs` instead

        Fill the form element inputs

        :param input_map: Dictionary mapping input names to the values to set
            them to. See
            :func:`webdriver_test_tools.webdriver.actions.form.fill_form_input`
            for values to use for different input types
        """
        warnings.warn(
            'FormObject.fill_form() is deprecated and may be removed in future versions, use fill_inputs() instead',
            DeprecationWarning
        )
        form = self.find_element(self.FORM_LOCATOR)
        actions.form.fill_form_inputs(self.driver, form, input_map)

    def fill_inputs(self, input_map, strict=False):
        """Fill form inputs

        :param input_map: Dictionary mapping input `name` key to the values to set
            them to. See :meth:`InputObject.set_value` for value formats for
            different input types
        :param strict: (Default = False) If True, throw an exception if a key
            in ``input_map`` is not a valid key in ``self.inputs``. Otherwise
            throw a warning and continue
        """
        for name, value in input_map.items():
            try:
                self.inputs[name].set_value(value)
            # TODO: verify
            except KeyError as e:
                if strict:
                    raise e
                else:
                    warnings.warn('Invalid input name {}, skipping'.format(e))

    # TODO: def get_input_values(self, name_list)

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

