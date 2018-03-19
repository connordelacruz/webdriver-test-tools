# Functions for test modules
import argparse
import unittest

from webdriver_test_tools import config
from webdriver_test_tools.project import test_loader, test_factory


def main(tests_module, config_module=None):
    """Function to call in test modules if __name__ == '__main__' at run time

    :param tests_module: The module object for <test_project>.tests
    :param config_module: (Optional) The module object for <test_project>.config. Will use webdriver_test_tools.config if not specified
    """
    # Fall back on default config module if test doesn't supply one
    if config_module is None:
        config_module = config
    # Older projects may not have the BrowserConfig class
    browser_config = config_module.BrowserConfig if 'BrowserConfig' in dir(config_module) else config.BrowserConfig
    # Parse arguments
    parser = get_parser(browser_config)
    args = parser.parse_args()
    # Handle --browser args
    if args.browser is None:
        browser_classes = [
            browser_class for browser_name, browser_class in browser_config.BROWSER_TEST_CLASSES.items()
        ]
    else:
        browser_classes = [
                browser_class for browser_name, browser_class in browser_config.BROWSER_TEST_CLASSES.items()
                if browser_name in args.browser
        ]
    test_name = args.test
    test_module_name = args.module
    # Run tests using parsed args
    run_tests(tests_module, config_module, browser_classes, test_name, test_module_name)


def get_parser(browser_config=None):
    """Returns the ArgumentParser object for use with main()

    :param browser_config: (Optional) BrowserConfig class for the project. Defaults to webdriver_test_tools.config.BrowserConfig if unspecified
    """
    parser = argparse.ArgumentParser()
    # Use default config if module is None or doesn't contain BrowserConfig class
    if browser_config is None:
        browser_config = config.BrowserConfig
    # Arguments for specifying browser to use
    browser_choices = [k for k in browser_config.BROWSER_TEST_CLASSES]
    parser.add_argument('-b', '--browser', nargs='+', choices=browser_choices, help='Run tests only in the specified browsers')
    # Arguments for specifying what test to run
    parser.add_argument('-t', '--test', help='Run a specific test case class or function', metavar='TestCase[.test_method]')
    # Arguments for specifying test module to run
    parser.add_argument('-m', '--module', help='Run only tests in a specific test module', metavar='test_module')
    return parser


def run_tests(tests_module, config_module, browser_classes=None, test_name=None, test_module_name=None):
    """Run tests using parsed args and project modules

    :param tests_module: The module object for <test_project>.tests
    :param config_module: The module object for <test_project>.config or webdriver_test_tools.config if not specified
    :param browser_classes: (Optional) List of browser test classes from parsed arg for --browser command line argument
    :param test_name: (Optional) Parsed arg for --test command line argument
    :param test_module_name: (Optional) Parsed arg for --module command line argument
    """
    # Enable graceful Ctrl+C handling
    unittest.installHandler()
    # Load WebDriverTestCase subclasses from project tests
    tests = test_loader.load_project_tests(tests_module, test_module_name)
    # Generate browser test cases from the loaded WebDriverTestCase classes
    browser_test_suite = test_factory.generate_browser_test_suite(tests, browser_classes, test_name)
    # Get configured test runner and run suite
    test_runner = config_module.TestSuiteConfig.get_runner()
    test_runner.run(browser_test_suite)



