# Functions for test modules
import argparse, unittest
from webdriver_test_tools.classes.webdriver_test_case import *
from webdriver_test_tools import config


def main(tests, test_runner=None):
    """Function to call in test modules if __name__ == '__main__' at run time

    :param tests: List of test case classes to generate tests for
    :param test_runner: (Optional) unittest test runner to use. Will use runner from
    webdriver_test_tools.config.TestSuiteConfig if not specified
    """
    parser = get_parser()
    args = parser.parse_args()
    browser_class = None if args.browser is None else BROWSER_TEST_CLASSES[args.browser]
    test_name = args.test
    unittest.installHandler()
    if test_runner is None:
        test_runner = config.TestSuiteConfig.get_runner()
    test_runner.run(generate_browser_test_suite(tests, browser_class, test_name))


def get_parser():
    """Returns the ArgumentParser object for use with main()"""
    parser = argparse.ArgumentParser()
    # Arguments for specifying browser to use
    browser_choices = [k for k in BROWSER_TEST_CLASSES]
    parser.add_argument('-b', '--browser', choices=browser_choices, help='Run tests only in the specified browser')
    # Arguments for specifying what test to run
    parser.add_argument('-t', '--test', help='Run a specific test case class or function', metavar='TestCase[.test_method]')
    return parser
