import webdriver_test_tools
from webdriver_test_tools.classes.webdriver_test_case import WebDriverTestCase, WebDriverMobileTestCase, Browsers
from framework_tests import config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
# Import actions subpackage
from webdriver_test_tools.webdriver import actions


# Test Case Classes

class FormActionsTestCase(WebDriverTestCase):
    """Test webdriver.actions.form submodule

    Since the purpose of this test is to interact with the page using framework functions
    and compare the outcome using WebDriver functions, page objects aren't used
    """

    # URL to go to at the start of each test
    SITE_URL = config.SiteConfig.BASE_URL + 'form.html'

    # Form locator
    FORM_LOCATOR = (By.ID, 'test-form')
    # Prefixes for names of optional, required, and disabled variants of the form inputs
    OPT_PREFIX = 'opt'
    REQ_PREFIX = 'req'
    DIS_PREFIX = 'dis'
    # Suffix of input names corresponding to the type of input
    TEXT = 'Text'
    RADIO = 'Radio'
    CHECKBOX = 'Checkbox'
    SELECT = 'Select'
    MULTIPLESELECT = 'MultipleSelect'
    # Values for radios and selects
    RADIO_VALS = ['1', '2']
    SELECT_OPTIONS = ['1', '2']
    MULTIPLESELECT_OPTIONS = ['1', '2', '3']

    def make_input_map(self, prefix=OPT_PREFIX):
        """Returns a map of input names to the desired values to set them to

        :param prefix: (Default = OPT_PREFIX) Name prefix for the type of input.
            ('opt' for optional inputs, 'req' for required inputs, 'dis' for
            disabled inputs)

        :return: Dictionary mapping input names to values to set them to
        """
        input_map = {
            prefix + self.TEXT: 'Test input',
            prefix + self.RADIO: self.RADIO_VALS[0],
            prefix + self.CHECKBOX: True,
            prefix + self.SELECT: self.SELECT_OPTIONS[0],
            prefix + self.MULTIPLESELECT: self.MULTIPLESELECT_OPTIONS[1:],
        }
        return input_map


    # Test Methods

    def test_fill_form_inputs(self):
        """Test actions.form.fill_form_inputs() on a variety of input types"""
        driver = self.driver
        form = driver.find_element(*self.FORM_LOCATOR)
        input_map = self.make_input_map()
        actions.form.fill_form_inputs(driver, form, input_map)

        input_name = self.OPT_PREFIX + self.TEXT
        expected_val = input_map[input_name]
        with self.subTest('Check text input', expected_val=expected_val):
            input_val = driver.find_element_by_name(input_name).get_attribute('value')
            self.assertEqual(expected_val, input_val)

        input_name = self.OPT_PREFIX + self.RADIO
        expected_val = input_map[input_name]
        with self.subTest('Check radio input', expected_val=expected_val):
            element = driver.find_element_by_css_selector('input[type="radio"][name="{}"]:checked'.format(input_name))
            input_val = element.get_attribute('value')
            self.assertEqual(expected_val, input_val)

        input_name = self.OPT_PREFIX + self.CHECKBOX
        expected_val = input_map[input_name]
        with self.subTest('Check checkbox input', expected_val=expected_val):
            input_val = driver.find_element_by_name(input_name).is_selected()
            self.assertEqual(expected_val, input_val)

        input_name = self.OPT_PREFIX + self.SELECT
        expected_val = input_map[input_name]
        with self.subTest('Check select input', expected_val=expected_val):
            input_val = driver.find_element_by_name(input_name).get_attribute('value')
            self.assertEqual(expected_val, input_val)

        input_name = self.OPT_PREFIX + self.MULTIPLESELECT
        expected_val = input_map[input_name]
        with self.subTest('Check multiple select input', expected_val=expected_val):
            select = Select(driver.find_element_by_name(input_name))
            input_val = [option.get_attribute('value') for option in select.all_selected_options]
            self.assertEqual(set(expected_val), set(input_val))



