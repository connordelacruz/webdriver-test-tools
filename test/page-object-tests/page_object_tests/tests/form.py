from selenium import webdriver
import webdriver_test_tools
from webdriver_test_tools.testcase import *

from page_object_tests import config
from page_object_tests.pages.form import TestFormObject


class FormObjectTestCase(WebDriverTestCase):
    """Test FormObject prototype"""

    # URL to go to at the start of each test
    SITE_URL = config.SiteConfig.BASE_URL + TestFormObject.PAGE_FILENAME

    # Test Methods

    # TODO: test_input_get_methods with pre-filled form

    def test_input_set_methods(self):
        """Test set_value() and get_value() methods"""
        form_object = TestFormObject(self.driver)
        input_map = {
            'optText': 'Sample text entry',
            'optRadio': '1',
            'optCheckbox': True,
            # 'optCheckboxGroup[]': ['1', '3'],
            'optSelect': '2',
            'optMultipleSelect': ['1', '3'],
        }
        # Fill form
        form_object.fill_inputs(input_map)
        # Assert that the input values match the retrieved values
        for input_name, set_val in input_map.items():
            get_val = form_object.inputs[input_name].get_value()
            with self.subTest('Call get_value() and compare with set_value() values', input_name=input_name, set_val=set_val, get_val=get_val):
                self.assertEqual(set_val, get_val)

