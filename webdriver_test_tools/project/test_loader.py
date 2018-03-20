# Load test cases from a project

import types
import unittest
from webdriver_test_tools.classes.webdriver_test_case import WebDriverTestCase


# TODO: pass a list of test cases?
def load_project_tests(tests_module, test_module_names=None):
    """Returns a list of WebDriverTestCase subclasses from all submodules in a test
    project's tests/ directory

    :param tests_module: The module object for <test_project>.tests
    :param test_module_names: (Optional) List of test module names. Only load test cases from a submodule of tests_module with the given names

    :return: A list of test classes from all test modules
    """
    test_list = []
    tests_module_attributes = dir(tests_module)
    if test_module_names is not None:
        tests_module_attributes = [name for name in tests_module_attributes if name in test_module_names]
    for name in tests_module_attributes:
        obj = getattr(tests_module, name)
        if isinstance(obj, types.ModuleType):
            test_list.extend(load_webdriver_test_cases(obj))
    return test_list


def load_webdriver_test_cases(module):
    """Returns a list of WebDriverTestCase subclasses from a module

    :param module: The module to load tests from

    :return: A list of test classes loaded from the module
    """
    test_list = []
    for name in dir(module):
        obj = getattr(module, name)
        if isinstance(obj, type) and issubclass(obj, WebDriverTestCase) and obj is not WebDriverTestCase:
            test_list.append(obj)
    return test_list


# TODO: re-work for multiple test methods
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


