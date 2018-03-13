# Functions for generating test cases

import unittest
from webdriver_test_tools.classes.webdriver_test_case import BROWSER_TEST_CLASSES


def generate_browser_test_suite(test_case_list, browser_test_class=None, test_name=None):
    """Generates test cases for multiple browsers and returns a TestSuite with all of the new tests

    :param test_case_list: A list of WebDriverTestCase subclasses to generate a test suite for
    :param browser_test_class: (Optional) If specified, only generate tests using this browser class. If not specified, tests will be generated for each available browser test case class.
    :param test_name: (Optional) Run only the specified test in each generated browser test case. This can be the name of the class (e.g. 'PrimaryNavTestCase') or the name of a single test method in a class (e.g. 'PrimaryNavTestCase.test_modal_links')

    :return: unittest.TestSuite object with generated tests for each browser
    """
    # if set, test_name could be 'TestCase' or 'TestCase.test_method'
    test_name_parts = None if test_name is None else test_name.split('.')
    # If test_name is specified, reduce test_case_list to just that test case
    if test_name_parts is not None:
        # test_name needs to have a test case name regardless of whether a function is specified
        test_case_list = [test_case for test_case in test_case_list if test_case.__name__ == test_name_parts[0]]
    browser_test_cases = []
    # Generate test classes for each test case in the list
    for test_case in test_case_list:
        browser_test_cases.extend(generate_browser_test_cases(test_case, browser_test_class))
    # if test_name is set, it could contain a specific test method to run
    test_method = None if test_name_parts is None or len(test_name_parts) < 2 else test_name_parts[1]
    # load tests from the generated classes and return a suite of them
    browser_tests = load_browser_tests(browser_test_cases, test_method)
    return unittest.TestSuite(browser_tests)


def load_browser_tests(browser_test_cases, test_method=None):
    """Load tests from browser test case classes

    :param browser_test_cases: List of generated browser test case classes
    :param test_method: (Optional) If specified, load only this test method from each browser test case

    :return: A list of loaded tests from the browser test cases
    """
    if test_method is not None:
        browser_tests = [browser_test_case(test_method) for browser_test_case in browser_test_cases]
    else:
        loader = unittest.TestLoader()
        browser_tests = [loader.loadTestsFromTestCase(browser_test_case) for browser_test_case in browser_test_cases]
    return browser_tests


def generate_browser_test_cases(base_class, browser_test_class=None):
    """Generate test cases for each browser from a WebDriverTestCase subclass

    :param base_class: The WebDriverTestCase subclass to generate test classes for
    :param browser_test_class: (Optional) If specified, only generate tests using this browser class. If not specified, tests will be generated for each available browser test case class

    :return: List of generated test case classes for each browser
    """
    # generate class only for browser_test_class if specified
    browser_classes = BROWSER_TEST_CLASSES.values() if browser_test_class is None else [browser_test_class, ]
    # iterate through a list of browser classes and generate test case
    browser_test_cases = [
        generate_browser_test_case(base_class, browser_class) for browser_class in browser_classes
    ]
    return browser_test_cases


def generate_browser_test_case(base_class, browser_test_class):
    """Generates a browser-specific test case class from a generic WebDriverTestCase

    :param base_class: WebDriverTestCase containing test functions
    :param browser_test_class: The driver-specific implementation of WebDriverTestCase to generate a test for
    """
    # Get base class name and docstring
    base_class_name = base_class.__name__
    base_class_doc = base_class.__doc__
    # generate new class with driver name appended to the class name and in parentheses at the start of the docstring
    new_class = type(base_class_name + browser_test_class.DRIVER_NAME, (base_class, browser_test_class),
                     {'__doc__': '({}) '.format(browser_test_class.DRIVER_NAME) + base_class_doc})
    return new_class
