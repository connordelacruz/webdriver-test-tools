# Functions for test modules
import argparse

from webdriver_test_tools import config
from webdriver_test_tools.classes.webdriver_test_case import *
from webdriver_test_tools.project import loader


def main(tests_module, test_suite_config=None):
    """Function to call in test modules if __name__ == '__main__' at run time

    :param tests_module: The module object for <test_project>.tests
    :param test_suite_config: (Optional) TestSuiteConfig class for the project. Will use webdriver_test_tools.config.TestSuiteConfig if not specified
    """
    parser = get_parser()
    args = parser.parse_args()
    browser_class = None if args.browser is None else BROWSER_TEST_CLASSES[args.browser]
    test_name = args.test
    test_module_name = args.module
    unittest.installHandler()
    if test_suite_config is None:
        test_suite_config = config.TestSuiteConfig
    test_runner = test_suite_config.get_runner()
    tests = loader.load_project_tests(tests_module, test_module_name)
    test_runner.run(generate_browser_test_suite(tests, browser_class, test_name))


def get_parser():
    """Returns the ArgumentParser object for use with main()"""
    parser = argparse.ArgumentParser()
    # Arguments for specifying browser to use
    browser_choices = [k for k in BROWSER_TEST_CLASSES]
    parser.add_argument('-b', '--browser', choices=browser_choices, help='Run tests only in the specified browser')
    # Arguments for specifying what test to run
    parser.add_argument('-t', '--test', help='Run a specific test case class or function', metavar='TestCase[.test_method]')
    # Arguments for specifying test module to run
    parser.add_argument('-m', '--module', help='Run only tests in a specific test module', metavar='test_module')
    return parser
