"""Functions for generating test cases"""

import unittest
from webdriver_test_tools.config import BrowserConfig
from webdriver_test_tools.project import test_loader
from webdriver_test_tools.classes.webdriver_test_case import WebDriverTestCase, WebDriverMobileTestCase, Browsers


def generate_browser_test_suite(test_case_list, browser_test_classes=None, test_class_map=None,
                                config_module=None, browserstack=False, headless=False):
    """Generates test cases for multiple browsers and returns a TestSuite with all of
    the new tests

    :param test_case_list: A list of WebDriverTestCase subclasses to generate a test
        suite for
    :param browser_test_classes: (Optional) If specified, only generate tests using the
        browser classes in this list. If not specified, tests will be generated for
        each available browser test case class.
    :param test_class_map: (Optional) Dictionary mapping test case names to a list of
        test functions. If the list is empty, all test functions will be loaded
    :param config_module: (Optional) The module object for <test_project>.config
    :param browserstack: (Default = False) If True, configure generated test cases to
        run on BrowserStack instead of locally. Need to provide `config_module` with
        appropriately configured `BrowserStackConfig` class if set to True
    :param headless: (Default = False) If True, configure driver to run tests in a
        headless browser. Tests will only be generated for drivers that support
        running headless browsers

    :return: unittest.TestSuite object with generated tests for each browser
    """
    # if headless, only use compatible browsers in browser_test_classes
    if headless:
        if browser_test_classes is None:
            browser_test_classes = Browsers.HEADLESS_COMPATIBLE.copy()
        else:
            browser_test_classes = [
                browser_test_class for browser_test_class in browser_test_classes if browser_test_class in Browsers.HEADLESS_COMPATIBLE
            ]
    browser_tests = []
    # Generate test classes for each test case in the list
    for test_case in test_case_list:
        generated_tests = generate_browser_test_cases(test_case, browser_test_classes, config_module, browserstack, headless)
        test_methods = None if test_class_map is None or test_case.__name__ not in test_class_map else test_class_map[test_case.__name__]
        loaded_tests = test_loader.load_browser_tests(generated_tests, test_methods)
        browser_tests.extend(loaded_tests)
    return unittest.TestSuite(browser_tests)


def generate_browser_test_cases(base_class, browser_test_classes=None, config_module=None,
                                browserstack=False, headless=False):
    """Generate test cases for each browser from a WebDriverTestCase subclass

    :param base_class: The WebDriverTestCase subclass to generate test classes for
    :param browser_test_classes: (Optional) If specified, only generate tests using the
        browser classes specified in this list. If not specified, tests will be
        generated for each available browser test case class
    :param config_module: (Optional) The module object for <test_project>.config
    :param browserstack: (Default = False) If True, configure generated test cases to
        run on BrowserStack instead of locally. Need to provide `config_module` with
        appropriately configured `BrowserStackConfig` class if set to True
    :param headless: (Default = False) If True, configure driver to run tests in a
        headless browser

    :return: List of generated test case classes for each browser
    """
    # generate class only for browser_test_class if specified
    browser_classes = BrowserConfig.BROWSER_TEST_CLASSES.values() if browser_test_classes is None else browser_test_classes
    # If this test is for non-mobile only, don't generate tests for subclasses of WebDriverMobileTestCase
    if base_class.SKIP_MOBILE:
        browser_classes = [
            browser_class for browser_class in browser_classes if not issubclass(browser_class, WebDriverMobileTestCase)
        ]
    # If this test is a subclass of WebDriverMobileTestCase, then only generate tests for subclasses of WebDriverMobileTestCase
    elif issubclass(base_class, WebDriverMobileTestCase):
        browser_classes = [
            browser_class for browser_class in browser_classes if issubclass(browser_class, WebDriverMobileTestCase)
        ]
    # iterate through a list of browser classes and generate test cases
    # skip browser classes if listed in base_class.SKIP_BROWSERS
    browser_test_cases = [
        generate_browser_test_case(base_class, browser_class, config_module, browserstack, headless) for browser_class in browser_classes
        if browser_class.SHORT_NAME not in base_class.SKIP_BROWSERS
    ]
    return browser_test_cases


def generate_browser_test_case(base_class, browser_test_class, config_module=None,
                               browserstack=False, headless=False):
    """Generates a browser-specific test case class from a generic WebDriverTestCase

    :param base_class: WebDriverTestCase containing test functions
    :param browser_test_class: The driver-specific implementation of WebDriverTestCase
        to generate a test for
    :param config_module: (Optional) The module object for <test_project>.config
    :param browserstack: (Default = False) If True, configure generated test cases to
        run on BrowserStack instead of locally. Need to provide `config_module` with
        appropriately configured `BrowserStackConfig` class if set to True
    :param headless: (Default = False) If True, configure driver to run tests in a
        headless browser

    :return: Test case class with tests from `base_class` and driver configurations from
        `browser_test_class`. If `browserstack` is set to True, returned class will have
        appropriate attributes configured for BrowserStack execution
    """
    # Get base class attributes
    base_class_name = base_class.__name__
    base_class_doc = base_class.__doc__
    base_class_module = base_class.__module__
    # Append the driver name portion of <Driver>TestCase to the class name
    browser_class_suffix = browser_test_class.__name__.replace('TestCase', '')
    new_class_name = base_class_name + browser_class_suffix
    # Use modified docstring and original module name from base class
    new_class_dict = {
        '__doc__': '({}) '.format(browser_test_class.DRIVER_NAME) + base_class_doc,
        '__module__': base_class_module,
    }
    # Use project's WebDriverConfig class if it exists
    if 'WebDriverConfig' in dir(config_module):
        new_class_dict['WebDriverConfig'] = config_module.WebDriverConfig
    new_class = type(new_class_name, (base_class, browser_test_class), new_class_dict)
    # Enable BrowserStack execution
    if browserstack:
        new_class = enable_browserstack(new_class, config_module)
    # Enable headless browsers
    if headless:
        new_class = enable_headless(new_class)
    return new_class


def enable_browserstack(browser_test_case, config_module):
    """Enable BrowserStack test execution for a class

    :param browser_test_case: Browser test case class to configure for BrowserStack
        usage
    :param config_module: The module object for <test_project>.config

    :return: browser_test_case class with `ENABLE_BS` and `COMMAND_EXECUTOR` attributes
        configured appropriately
    """
    # Raise exception if somehow this method was called but BrowserStack is not configured/enabled
    if 'BrowserStackConfig' not in dir(config_module) or not config_module.BrowserStackConfig.ENABLE:
        raise Exception('BrowserStack is not enabled or BrowserStackConfig class could not be found.')
    bs_config = config_module.BrowserStackConfig
    browser_test_case.ENABLE_BS = True
    browser_test_case.COMMAND_EXECUTOR = bs_config.get_command_executor()
    bs_config.add_browserstack_capabilities(browser_test_case.CAPABILITIES)
    return browser_test_case


def enable_headless(browser_test_case):
    """Enable headless browser test execution for a class

    :param browser_test_case: Browser test case class to configure for BrowserStack
        usage

    :return: browser_test_case class with `ENABLE_HEADLESS` attribute configured
    """
    browser_test_case.ENABLE_HEADLESS = True
    return browser_test_case


