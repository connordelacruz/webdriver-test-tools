"""Load test cases from a project."""

import fnmatch
import re
import types
import unittest

from webdriver_test_tools.testcase import *

# Exceptions

class TestLoaderException(Exception):
    """Base exception class for the test_loader module"""
    pass


class TestMethodsNotFoundException(TestLoaderException):
    """Exception raised if no test methods matching the specified criteria were
    found in a test case class
    """
    pass


class TestCasesNotFoundException(TestLoaderException):
    """Exception raised if no test cases matching the specified criteria are
    found
    """
    pass


# Loader Methods

def load_project_tests(tests_module,
                       test_module_names=None, test_class_map=None, skip_class_map=None):
    """Returns a list of :class:`WebDriverTestCase
    <webdriver_test_tools.testcase.webdriver.WebDriverTestCase>` subclasses
    from all submodules in a test project's tests/ directory

    If ``test_class_map`` or ``skip_class_map`` contain wildcards in any of
    their keys, those will be expanded into keys for each test class name that
    matches, altering the original dictionaries as a side effect.

    :param tests_module: The module object for ``<test_project>.tests``
    :param test_module_names: (Optional) List of test module names. Only load
        test cases from a submodule of ``tests_module`` with the given names
    :param test_class_map: (Optional) Dictionary mapping test class names (or
        wildcard strings) to a list of method names or an empty list if the
        whole class should be run. Only load test cases that match the keys in
        this dictionary
    :param skip_class_map: (Optional) Dictionary mapping test class names (or
        wildcard strings) to a list of method names or an empty list if the
        whole class should be skipped. Skip test cases that match the keys in
        this dictionary if they're mapped to an empty list. If one or more
        methods are specified to skip, it's possible that there are more
        methods in the class that should be run

    :return: A list of test classes from all test modules
    """
    test_module_list = get_test_modules(tests_module, test_module_names)
    test_case_list = get_test_cases(test_module_list)
    # Expand any wildcard keys in class maps prior to filtering
    test_class_map, skip_class_map = expand_wildcard_class_names(
        test_case_list, test_class_map, skip_class_map
    )
    # Filter list of test cases based on class maps
    return filter_test_cases(test_case_list, test_class_map, skip_class_map)


def get_test_modules(tests_module, test_module_names=None):
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


def get_test_cases(test_module_list):
    """Returns a list of valid test cases from a list of test modules

    :param test_module_list: List of test modules to retrieve test cases from

    :return: List of valid test cases from the test modules
    """
    test_case_list = []
    for module in test_module_list:
        test_case_list.extend(_get_module_test_cases(module))
    return test_case_list


def _get_module_test_cases(module):
    """Returns a list of valid test cases from a test module

    :param module: Test module to retrieve test cases from

    :return: List of valid test cases from a test module
    """
    return [
        attr for attr in [getattr(module, name) for name in dir(module)]
        if _is_valid_case(attr)
    ]


def expand_wildcard_class_names(test_case_list, test_class_map=None, skip_class_map=None):
    """Update any entries in ``test_class_map`` and ``skip_class_map`` with
    wildcards as keys

    Adds keys for each matching class name mapped to the same method lists from
    the wildcard key, then removes all wildcard keys after expanding

    :param test_case_list: List of all test cases at this point
    :param test_class_map: (Optional) Dictionary mapping test class names (or
        wildcard strings) to a list of method names or an empty list if the
        whole class should be run
    :param skip_class_map: (Optional) Dictionary mapping test class names (or
        wildcard strings) to a list of method names or an empty list if the
        whole class should be skipped

    :return: The modified ``test_class_map`` and ``skip_class_map`` as a tuple.
        Either map may be set to ``None`` if expanding wildcards caused the map
        to be empty (i.e. it was all wildcards and none of them matched any
        test cases)

    :raises TestCasesNotFoundException: if ``test_class_map`` was not empty
        before wildcard expansion but is empty after. This is to override the
        default behavior of running all tests if ``test_class_map`` is empty,
        because presumably the user wanted to only run a specific subset of
        tests (otherwise ``test_class_map`` would have been empty to begin
        with)
    """
    if test_class_map:
        test_class_map = _expand_wildcard_class_map_keys(test_case_list, test_class_map)
        # If test_class_map evaluates to False after expansion, then there were
        # wildcard keys specified and none of them matched. The default
        # behaviour for an empty test_class_map is to run all tests, but
        # presumably the user wanted to limit this to a subset since the
        # specified 1 or more test cases
        if not test_class_map:
            raise TestCasesNotFoundException(
                'No valid test case classes found after wildcard expansion'
            )
    if skip_class_map:
        skip_class_map = _expand_wildcard_class_map_keys(test_case_list, skip_class_map)
    # Entries should be updated anyway, so this return value shouldn't be necessary
    return test_class_map, skip_class_map


def _expand_wildcard_class_map_keys(test_case_list, test_class_map):
    """Updates any entries in a test class map with wildcards as keys

    Adds keys for each matching class name mapped to the same method lists from
    the wildcard key, then removes all wildcard keys after expanding

    :param test_case_list: List of all test cases at this point
    :param test_class_map: Dictionary mapping test class names (or wildcard
        strings) to a list of method names

    :return: The modified ``test_class_map`` or ``None`` if the updated map is
        empty (i.e. it was all wildcards and none of them matched any test
        cases)
    """
    # Get list of wildcard keys
    wildcard_names = [key for key in test_class_map if '*' in key]
    # Temporary map of class names to the class
    class_name_map = {
        test_case.__name__: test_case for test_case in test_case_list
    }
    # Temporary map used to update the original after going through the
    # wildcards. The keys to this one will be the matching class names mapped
    # to the appropriate method lists
    updated_class_map = {}
    for wildcard_name in wildcard_names:
        matching_names = fnmatch.filter(class_name_map, wildcard_name)
        # Update temporary map with matching classname: method list from wildcard entry
        updated_class_map.update({
            matching_name: [method for method in test_class_map[wildcard_name]]
            for matching_name in matching_names
        })
        # Pop wildcard name from original map after finishing
        test_class_map.pop(wildcard_name)
    # If any matching names are existing keys, copy those method lists
    existing_keys = [key for key in updated_class_map if key in test_class_map]
    for existing_key in existing_keys:
        updated_class_map[existing_key].extend(test_class_map[existing_key])
    # Update original map with temp dictionary
    # TODO: Look into issues with overlapping class wildcards
    test_class_map.update(updated_class_map)
    # If none of the wild card entries matched any tests and the updated map is
    # empty, set it to None
    if not test_class_map:
        test_class_map = None
    # Entries should be updated anyway, so this return value shouldn't be necessary
    return test_class_map


def filter_test_cases(test_case_list,
                      test_class_map=None, skip_class_map=None):
    """Returns a list of test cases filtered by --test and --skip arguments

    :param test_case_list: List of test case classes to filter
    :param test_class_map: (Optional) List of test case class names to load.
        Will load all if unspecified
    :param skip_class_map: (Optional) List of test case class names to skip.
        Will skip none if unspecified

    :return: List of test case classes filtered based on the --test/--skip
        arguments
    """
    # Reduce set of tests to the specified classes (if applicable)
    if test_class_map is not None:
        expr = '|'.join(fnmatch.translate(p) for p in test_class_map)
        test_case_list = [test_case for test_case in test_case_list if re.match(expr, test_case.__name__)]
    # Remove skipped classes (if applicable)
    # Only filter classes with no function lists
    # (these are the ones that should be skipped entirely)
    skip_class_names = _get_skip_class_names(skip_class_map)
    if skip_class_names:
        expr = '|'.join(fnmatch.translate(p) for p in skip_class_names)
        test_case_list = [test_case for test_case in test_case_list if not re.match(expr, test_case.__name__)]
    return test_case_list


def _get_skip_class_names(skip_class_map):
    """Returns list of class names to skip

    Returned list only contains names of classes where all methods are skipped.
    If skip_class_map is None, returns None

    :param skip_class_map: Result of passing parsed arg for --skip command line
        argument to parse_test_names()

    :return: List of class names to skip
    """
    if skip_class_map:
        return [
            class_name for class_name, methods in skip_class_map.items() if not methods
        ]
    return None


def _is_valid_case(obj):
    """Returns True if ``obj`` is a valid test case

    Criteria for being a valid test case:

        - Is a class and a subclass of :class:`WebDriverTestCase
          <webdriver_test_tools.testcase.webdriver.WebDriverTestCase>`
        - Is not :class:`WebDriverTestCase
          <webdriver_test_tools.testcase.webdriver.WebDriverTestCase>` or
          :class:`WebDriverMobileTestCase
          <webdriver_test_tools.testcase.webdriver.WebDriverMobileTestCase>`

    :param obj: The object to validate

    :return: True if ``obj`` is a valid test case, False if not
    """
    parent_classes = [WebDriverTestCase, WebDriverMobileTestCase]
    # Load class if it subclasses WebDriverTestCase (but don't load WebDriverTestCase itself)
    return (isinstance(obj, type)
            and issubclass(obj, WebDriverTestCase)
            and obj not in parent_classes)


def load_browser_tests(base_class, generated_test_cases,
                       test_methods=None, skip_methods=None):
    """Load tests from browser test case classes

    :param base_class: The base test case class that the generated test cases
        are based on. Used to expand any wildcards in ``test_methods`` or
        ``skip_methods`` to valid test methods
    :param generated_test_cases: List of generated browser test case classes
        for a single subclass of :class:`WebDriverTestCase
        <webdriver_test_tools.testcase.webdriver.WebDriverTestCase>`
    :param test_methods: (Optional) List of test method names (or wildcard
        strings). If specified, load only these test methods from each browser
        test case
    :param skip_methods: (Optional) List of test method names (or wildcard
        strings). If specified, do not load these test methods from each
        browser test case

    :return: A list of loaded tests from the browser test cases
    """
    loader = unittest.TestLoader()
    # Expand any wildcard methods prior to loading
    try:
        test_methods, skip_methods = expand_wildcard_method_names(
            loader, base_class, test_methods, skip_methods
        )
    except TestMethodsNotFoundException as e:
        # test_methods was not empty prior to wildcard expansion and was empty after,
        # so don't generate browser test cases
        # TODO: print warning?
        return []
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
        browser_tests = [
            browser_test_case(test_method)
            for browser_test_case in generated_test_cases
            for test_method in loader.getTestCaseNames(browser_test_case)
            if test_method not in skip_methods
        ]
    return browser_tests


def expand_wildcard_method_names(loader, base_class, test_methods=None, skip_methods=None):
    """Update any entries in ``test_methods`` and ``skip_methods`` with wildcards

    Adds list entries for matching methods in ``base_class``, then removes all
    wildcard entries after expanding. Additionally, any duplicate
    entries in the list after wildcard expansion will be removed so the same
    test method isn't run multiple times

    :param loader: ``unittest.TestLoader`` object. Used to list all test
        methods from ``base_class``
    :param base_class: The base test case class. Used to get a list of all test
        methods when searching for matches
    :param test_methods: (Optional) List of test method names (or wildcard
        strings) to run
    :param skip_methods: (Optional) List of test method names (or wildcard
        strings) to skip

    :return: The modified ``test_methods`` and ``skip_methods`` as a tuple.
        Either of these may be set to ``None`` if expanding wildcards caused
        the list to be empty (i.e. it was all wildcards and none of them
        matched any test methods)

    :raises TestMethodsNotFoundException: if ``test_methods`` was not empty
        before wildcard expansion but is empty after. This is to override the
        default behavior of running all test methods if ``test_methods`` is
        empty, because presumably the user wanted to only run a specific subset
        of tests (otherwise ``test_methods`` would have been empty to begin
        with)
    """
    # List of test methods in the base class
    base_class_methods = loader.getTestCaseNames(base_class)
    if test_methods:
        test_methods = _expand_wildcard_method_list_items(base_class_methods, test_methods)
        # If test_methods evaluates to False after expansion, then there were
        # wildcard methods specified and none of them matched. The default
        # behavior for an empty test_methods list is to run all methods, but
        # presumably the user wanted to limit this to a subset since they
        # specified 1 or more methods
        if not test_methods:
            raise TestMethodsNotFoundException(
                'No valid test methods found after test wildcard expansion for {}'.format(base_class.__name__)
            )
    if skip_methods:
        skip_methods = _expand_wildcard_method_list_items(base_class_methods, skip_methods)
    # Entries should be updated anyway, so this return value shouldn't be necessary
    return test_methods, skip_methods


def _expand_wildcard_method_list_items(base_class_methods, test_methods):
    """Updates any entries in a test/skip method list with wildcards

    Adds list entries for each test method that matches a wildcard entry, then
    removes all wildcard entries after expanding. Additionally, any duplicate
    entries in the list after wildcard expansion will be removed so the same
    test method isn't run multiple times

    :param base_class_methods: List of all test methods in the test case class
        (i.e. result of loader.getTestCaseNames())
    :param test_methods: List of test case method names (or wildcard strings)

    :return: The modified ``test_methods`` list or ``None`` if the updated list
        is empty (i.e. it was all wildcards and none of them matched any test
        methods)
    """
    # Get list of wildcard test methods
    wildcard_methods = [method for method in test_methods]
    # Temporary list of matching test methods used to update the original
    updated_test_methods = []
    for wildcard_method in wildcard_methods:
        matching_methods = fnmatch.filter(base_class_methods, wildcard_method)
        # Update temporary list with matching test methods
        updated_test_methods.extend(matching_methods)
        # Remove wildcard name from original list after finishing
        test_methods.remove(wildcard_method)
    # Update original list
    test_methods.extend(updated_test_methods)
    # Remove duplicate entries (convert from a list to a dict and back)
    test_methods = list(dict.fromkeys(test_methods))
    # If none of the wildcard entries matched any test methods and the updated list is empty, set it to None
    if not test_methods:
        test_methods = None
    return test_methods

