# Load test cases from a project

import types
from webdriver_test_tools.classes.webdriver_test_case import WebDriverTestCase


def load_project_tests(tests_module, test_module_name=None):
    """Returns a list of WebDriverTestCase subclasses from all submodules in a test
    project's tests/ directory

    :param tests_module: The module object for <test_project>.tests
    :param test_module_name: (Optional) Only load test cases from a submodule of tests_module with the given name

    :return: A list of test classes from all test modules
    """
    test_list = []
    tests_module_attributes = dir(tests_module)
    if test_module_name is not None:
        tests_module_attributes = [name for name in tests_module_attributes if name == test_module_name]
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
        if isinstance(obj, type) and issubclass(obj, WebDriverTestCase) and not obj is WebDriverTestCase:
            test_list.append(obj)
    return test_list



