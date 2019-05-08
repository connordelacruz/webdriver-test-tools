from selenium import webdriver
import webdriver_test_tools
from webdriver_test_tools.testcase import *

from page_object_tests import config
from page_object_tests.pages.form import YAMLForm, NoYAMLForm


class FormObjectTestCase(WebDriverTestCase):
    """Test FormObject prototype"""

    # URL to go to at the start of each test
    SITE_URL = config.SiteConfig.BASE_URL + YAMLForm.PAGE_FILENAME

    # Test Methods

    # TODO: test_input_get_methods with pre-filled form

    def test_input_set_methods_yaml(self):
        """Test set_value() and get_value() methods (YAML)"""
        form_object = YAMLForm(self.driver)
        self._test_input_set_methods(form_object)

    def test_input_set_methods_no_yaml(self):
        """Test set_value() and get_value() methods (no YAML)"""
        form_object = NoYAMLForm(self.driver)
        self._test_input_set_methods(form_object)

    def _test_input_set_methods(self, form_object):
        # Subtest message format string
        subtest_msg_fmt = 'Call get_value() and compare with values used in fill_form() [{val_type} value input types]'
        # Single value input types
        input_map = {
            'optText': 'Sample text entry',
            'optRadio': '1',
            'optCheckbox': True,
            'optSelect': '2',
        }
        form_object.fill_inputs(input_map)
        for input_name, set_val in input_map.items():
            get_val = form_object.inputs[input_name].get_value()
            with self.subTest(subtest_msg_fmt.format(val_type='single'),
                              input_name=input_name, set_val=set_val, get_val=get_val):
                self.assertEqual(set_val, get_val)

        # Dictionary value input types
        input_map = {
            'optCheckboxGroup[]': {'1': True, '3': True},
        }
        form_object.fill_inputs(input_map)
        for input_name, set_val in input_map.items():
            get_val = form_object.inputs[input_name].get_value()
            for key, val in set_val.items():
                with self.subTest(subtest_msg_fmt.format(val_type='dictionary'),
                                  input_name=input_name, set_val=set_val, get_val=get_val):
                    self.assertIn(
                        key, get_val,
                        msg='Key from set value dictionary not in dictionary returned by get_value()'
                    )
                    self.assertEqual(
                        val, get_val[key], msg='set_value() and get_value() for key do not match'
                    )

        # List value input types
        input_map = {
            'optMultipleSelect': ['1', '3'],
        }
        form_object.fill_inputs(input_map)
        for input_name, set_val in input_map.items():
            get_val = form_object.inputs[input_name].get_value()
            with self.subTest(subtest_msg_fmt.format(val_type='list'),
                              input_name=input_name, set_val=set_val, get_val=get_val):
                # assertCountEqual() compares lists regardless of order
                self.assertCountEqual(set_val, get_val)

