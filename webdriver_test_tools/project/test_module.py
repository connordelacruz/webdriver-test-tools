# Functions for test modules
import argparse
import unittest

from webdriver_test_tools import config
# TODO: remove import once config is implemented
from webdriver_test_tools.classes.webdriver_test_case import BROWSER_TEST_CLASSES
from webdriver_test_tools.project import test_loader, test_factory


def main(tests_module, config_module=None):
    """Function to call in test modules if __name__ == '__main__' at run time

    :param tests_module: The module object for <test_project>.tests
    :param config_module: (Optional) The module object for <test_project>.config. Will use webdriver_test_tools.config if not specified
    """
    parser = get_parser(config_module)
    args = parser.parse_args()
    # TODO: update to use config_module
    if args.browser is None:
        browser_classes = None
    else:
        browser_classes = [browser_class for browser_name, browser_class in BROWSER_TEST_CLASSES.items() if browser_name in args.browser]
    test_name = args.test
    test_module_name = args.module
    unittest.installHandler()
    if config_module is None:
        config_module = config
    # Load WebDriverTestCase subclasses from project tests
    tests = test_loader.load_project_tests(tests_module, test_module_name)
    # Generate browser test cases from the loaded WebDriverTestCase classes
    browser_test_suite = test_factory.generate_browser_test_suite(tests, browser_classes, test_name)
    test_runner = config_module.TestSuiteConfig.get_runner()
    test_runner.run(browser_test_suite)


def get_parser(config_module=None):
    """Returns the ArgumentParser object for use with main()"""
    parser = argparse.ArgumentParser()
    # Use default config if module is None or doesn't contain BrowserConfig class
    if config_module is None or not 'BrowserConfig' in dir(config_module):
        config_module = config
    # Arguments for specifying browser to use
    browser_choices = [k for k in config_module.BrowserConfig.BROWSER_TEST_CLASSES]
    parser.add_argument('-b', '--browser', nargs='+', choices=browser_choices, help='Run tests only in the specified browsers')
    # Arguments for specifying what test to run
    parser.add_argument('-t', '--test', help='Run a specific test case class or function', metavar='TestCase[.test_method]')
    # Arguments for specifying test module to run
    parser.add_argument('-m', '--module', help='Run only tests in a specific test module', metavar='test_module')
    return parser
