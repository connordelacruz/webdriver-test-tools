# Load test cases from a project

import types
import unittest
from webdriver_test_tools.classes.webdriver_test_case import WebDriverTestCase, WebDriverMobileTestCase


def load_project_tests(tests_module, test_class_names=None, test_module_names=None):
    """Returns a list of WebDriverTestCase subclasses from all submodules in a test
    project's tests/ directory

    :param tests_module: The module object for <test_project>.tests
    :param test_class_names: (Optional) List of test class names. Only load test cases with these names
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
            test_list.extend(load_webdriver_test_cases(obj, test_class_names))
    return test_list


def load_webdriver_test_cases(module, test_class_names=None):
    """Returns a list of WebDriverTestCase subclasses from a module

    :param module: The module to load tests from
    :param test_class_names: (Optional) List of test case class names to load. Will load all if unspecified

    :return: A list of test classes loaded from the module
    """
    test_list = []
    for name in dir(module):
        obj = getattr(module, name)
        # Load class if it subclasses WebDriverTestCase (but don't load WebDriverTestCase itself)
        if isinstance(obj, type) and issubclass(obj, WebDriverTestCase) and obj is not WebDriverTestCase and obj is not WebDriverMobileTestCase:
            # If test_class_names is specified, only load test cases whose names are specified
            if test_class_names is None or name in test_class_names:
                test_list.append(obj)
    return test_list


def load_browser_tests(generated_test_cases, test_methods=None):
    """Load tests from browser test case classes

    :param generated_test_cases: List of generated browser test case classes for a single subclass of WebDriverTestCase
    :param test_methods: (Optional) List of test method names. If specified, load only these test methods from each browser test case

    :return: A list of loaded tests from the browser test cases
    """
    # If test_methods is not None and is not empty, load only the specified test methods
    if test_methods:
        browser_tests = [browser_test_case(test_method) for test_method in test_methods for browser_test_case in generated_test_cases]
    # Else load all test methods from each
    else:
        loader = unittest.TestLoader()
        browser_tests = [loader.loadTestsFromTestCase(browser_test_case) for browser_test_case in generated_test_cases]
    return browser_tests


