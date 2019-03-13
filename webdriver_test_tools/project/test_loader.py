"""Load test cases from a project."""

import fnmatch
import re
import types
import unittest

from webdriver_test_tools.testcase import *

# TODO: make sure module is organized

# TODO: Update docs
# TODO: Ensure that changes don't break function stuff
def load_project_tests(tests_module,
                       test_module_names=None, test_class_names=None, skip_class_names=None):
    """Returns a list of :class:`WebDriverTestCase
    <webdriver_test_tools.testcase.webdriver.WebDriverTestCase>` subclasses
    from all submodules in a test project's tests/ directory

    :param tests_module: The module object for ``<test_project>.tests``
    :param test_module_names: (Optional) List of test module names. Only load
        test cases from a submodule of ``tests_module`` with the given names
    :param test_class_names: (Optional) List of test class names. Only load
        test cases with these names
    :param skip_class_names: (Optional) List of test class names. Skip test
        cases with these names

    :return: A list of test classes from all test modules
    """
    test_module_list = _get_test_modules(tests_module, test_module_names)
    test_case_list = _get_test_cases(test_module_list)
    # for test_module in _get_test_modules(tests_module, test_module_names):
    #     test_case_list.extend(
    #         load_webdriver_test_cases(test_module, test_class_names, skip_class_names)
    #     )
    return _filter_test_cases(test_case_list, test_class_names, skip_class_names)


def _get_test_modules(tests_module, test_module_names=None):
    """Returns a list of submodules in a test project's tests/ directory

    :param tests_module: The module object for ``<test_project>.tests``
    :param test_module_names: (Optional) List of test module names. Only load
        test cases from a submodule of ``tests_module`` with the given names

    :return: A list of test modules
    """
    # Get a list of all attributes from tests_module (skipping pkgutil)
    tests_module_attributes = [
        attr for attr in dir(tests_module) if attr != 'pkgutil'
    ]
    # Filter attributes based on test_module_names (if provided)
    if test_module_names is not None:
        tests_module_attributes = [
            name for name in tests_module_attributes if name in test_module_names
        ]
    # Return list of valid submodules of tests_module
    return [
        attr for attr in [
            getattr(tests_module, name) for name in tests_module_attributes
        ] if isinstance(attr, types.ModuleType)
    ]


def _get_module_test_cases(module):
    """Returns a list of valid test cases from a test module

    :param module: Test module to retrieve test cases from

    :return: List of valid test cases from a test module
    """
    return [
        attr for attr in [getattr(module, name) for name in dir(module)]
        if _is_valid_case(attr)
    ]


def _get_test_cases(test_module_list):
    """Returns a list of valid test cases from a list of test modules

    :param test_module_list: List of test modules to retrieve test cases from

    :return: List of valid test cases from the test modules
    """
    test_case_list = []
    for module in test_module_list:
        test_case_list.extend(_get_module_test_cases(module))
    return test_case_list


def _filter_test_cases(test_case_list, test_class_names=None, skip_class_names=None):
    # TODO: doc and implement
    # TODO: merge steps into a single regex
    # Reduce set of tests to the specified classes (if applicable)
    if test_class_names is not None:
        expr = '|'.join(fnmatch.translate(p) for p in test_class_names)
        test_case_list = [test_case for test_case in test_case_list if re.match(expr, test_case.__name__)]
    # Remove skipped classes (if applicable)
    if skip_class_names is not None:
        expr = '|'.join(fnmatch.translate(p) for p in skip_class_names)
        test_case_list = [test_case for test_case in test_case_list if not re.match(expr, test_case.__name__)]
    return test_case_list


# TODO: re-work? remove?
def load_webdriver_test_cases(module,
                              test_class_names=None, skip_class_names=None):
    """Returns a list of :class:`WebDriverTestCase
    <webdriver_test_tools.testcase.webdriver.WebDriverTestCase>` subclasses
    from a module

    :param module: The module to load tests from
    :param test_class_names: (Optional) List of test case class names to load.
        Will load all if unspecified
    :param skip_class_names: (Optional) List of test case class names to skip.
        Will skip none if unspecified

    :return: A list of test classes loaded from the module
    """
    return [
        attr for attr in [getattr(module, name) for name in dir(module)]
        if _is_valid_case(attr, test_class_names, skip_class_names)
    ]


# TODO: only check if obj meets test case criteria?
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
    return (isinstance(obj, type) and issubclass(obj, WebDriverTestCase) and obj not in parent_classes
            and (skip_class_names is None or obj.__name__ not in skip_class_names)
            and (test_class_names is None or obj.__name__ in test_class_names))


# TODO: wildcard support for test functions
def load_browser_tests(generated_test_cases,
                       test_methods=None, skip_methods=None):
    """Load tests from browser test case classes

    :param generated_test_cases: List of generated browser test case classes
        for a single subclass of :class:`WebDriverTestCase
        <webdriver_test_tools.testcase.webdriver.WebDriverTestCase>`
    :param test_methods: (Optional) List of test method names. If specified,
        load only these test methods from each browser test case
    :param skip_methods: (Optional) List of test method names. If specified, do
        not load these test methods from each browser test case

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

