"""Load test cases from a project."""

import types
import unittest

from webdriver_test_tools.testcase import *


def load_project_tests(tests_module, test_module_names=None, test_class_names=None, skip_class_names=None):
    """Returns a list of :class:`WebDriverTestCase <webdriver_test_tools.testcase.webdriver.WebDriverTestCase>`
    subclasses from all submodules in a test project's tests/ directory

    :param tests_module: The module object for ``<test_project>.tests``
    :param test_module_names: (Optional) List of test module names. Only load test cases from a submodule of
        ``tests_module`` with the given names
    :param test_class_names: (Optional) List of test class names. Only load test cases with these names
    :param skip_class_names: (Optional) List of test class names. Skip test cases with these names

    :return: A list of test classes from all test modules
    """
    test_list = []
    tests_module_attributes = dir(tests_module)
    if test_module_names is not None:
        tests_module_attributes = [name for name in tests_module_attributes if name in test_module_names]
    for name in tests_module_attributes:
        obj = getattr(tests_module, name)
        if isinstance(obj, types.ModuleType):
            test_list.extend(load_webdriver_test_cases(obj, test_class_names, skip_class_names))
    return test_list


def load_webdriver_test_cases(module, test_class_names=None, skip_class_names=None):
    """Returns a list of :class:`WebDriverTestCase <webdriver_test_tools.testcase.webdriver.WebDriverTestCase>`
    subclasses from a module

    :param module: The module to load tests from
    :param test_class_names: (Optional) List of test case class names to load. Will load all if unspecified
    :param skip_class_names: (Optional) List of test case class names to skip. Will skip none if unspecified

    :return: A list of test classes loaded from the module
    """
    test_list = []
    for name in dir(module):
        obj = getattr(module, name)
        # Load class if it subclasses WebDriverTestCase (but don't load WebDriverTestCase itself)
        if _is_valid_case(obj, test_class_names, skip_class_names):
            test_list.append(obj)
    return test_list


def _is_valid_case(obj, test_class_names=None, skip_class_names=None):
    """Returns True if ``obj`` is a valid test case

    Criteria for being a valid test case:

        - Is a class and a subclass of :class:`WebDriverTestCase
          <webdriver_test_tools.testcase.webdriver.WebDriverTestCase>`
        - Is not :class:`WebDriverTestCase
          <webdriver_test_tools.testcase.webdriver.WebDriverTestCase>` or
          :class:`WebDriverMobileTestCase
          <webdriver_test_tools.testcase.webdriver.WebDriverMobileTestCase>`
        - Is not listed in ``skip_class_names`` (if provided)
        - Is listed in ``test_class_names`` (if provided)

    :param obj: The object to validate
    :param test_class_names: (Optional) Names of test classes to run
    :param skip_class_names: (Optional) Names of test classes to skip

    :return: True if ``obj`` is a valid test case, False if not
    """
    parent_classes = [WebDriverTestCase, WebDriverMobileTestCase]
    # Load class if it subclasses WebDriverTestCase (but don't load WebDriverTestCase itself)
    if (isinstance(obj, type) and issubclass(obj, WebDriverTestCase) and obj not in parent_classes
            and (skip_class_names is None or obj.__name__ not in skip_class_names)
            and (test_class_names is None or obj.__name__ in test_class_names)
    ):
        return True
    return False


def load_browser_tests(generated_test_cases, test_methods=None, skip_methods=None):
    """Load tests from browser test case classes

    :param generated_test_cases: List of generated browser test case classes for a single subclass of
        :class:`WebDriverTestCase <webdriver_test_tools.testcase.webdriver.WebDriverTestCase>`
    :param test_methods: (Optional) List of test method names. If specified, load only these test methods from each
        browser test case
    :param skip_methods: (Optional) List of test method names. If specified, do not load these test methods from
        each browser test case

    :return: A list of loaded tests from the browser test cases
    """
    if skip_methods is None:
        skip_methods = []
    # If test_methods is not None and is not empty, load only the specified test methods
    if test_methods:
        browser_tests = [
            browser_test_case(test_method) for test_method in test_methods
            for browser_test_case in generated_test_cases
            if test_method not in skip_methods
        ]
    # Else load all test methods from each
    else:
        loader = unittest.TestLoader()
        browser_tests = [
            browser_test_case(test_method)
            for browser_test_case in generated_test_cases
            for test_method in loader.getTestCaseNames(browser_test_case)
            if test_method not in skip_methods
        ]
    return browser_tests
