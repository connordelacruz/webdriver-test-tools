# Functions for test modules
import argparse
import unittest

from webdriver_test_tools import config
from webdriver_test_tools.project import test_loader, test_factory


def main(tests_module, config_module=None):
    """Function to call in test modules if __name__ == '__main__' at run time

    :param tests_module: The module object for <test_project>.tests
    :param config_module: (Optional) The module object for <test_project>.config. Will
        use webdriver_test_tools.config if not specified
    """
    # Fall back on default config module if test doesn't supply one
    if config_module is None:
        config_module = config
    # Older projects may not have the BrowserConfig class
    browser_config = config_module.BrowserConfig if 'BrowserConfig' in dir(config_module) else config.BrowserConfig
    browserstack_config = config_module.BrowserStackConfig if 'BrowserStackConfig' in dir(config_module) else config.BrowserStackConfig
    # Parse arguments
    parser = get_parser(browser_config, browserstack_config)
    args = parser.parse_args()
    # handle --browserstack arg if enabled
    browserstack = 'browserstack' in dir(args) and args.browserstack
    # Determine what config class to use based on --browserstack arg
    browser_config_class = browserstack_config if browserstack else browser_config
    # Handle --browser args
    if args.browser is None:
        browser_classes = [
            browser_class for browser_name, browser_class in browser_config_class.BROWSER_TEST_CLASSES.items()
        ]
    else:
        browser_classes = [
            browser_class for browser_name, browser_class in browser_config_class.BROWSER_TEST_CLASSES.items()
            if browser_name in args.browser
        ]
    test_class_map = parse_test_names(args.test)
    test_module_names = args.module
    # Run tests using parsed args
    run_tests(tests_module, config_module, browser_classes, test_class_map, test_module_names, browserstack)


def get_parser(browser_config=None, browserstack_config=None):
    """Returns the ArgumentParser object for use with main()

    :param browser_config: (Optional) BrowserConfig class for the project. Defaults to
        webdriver_test_tools.config.BrowserConfig if unspecified
    :param browserstack_config: (Optional) BrowserStackConfig class for the project.
        Defaults to webdriver_test_tools.config.BrowserStackConfig if unspecified
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    # Use default config if module is None or doesn't contain BrowserConfig class
    if browser_config is None:
        browser_config = config.BrowserConfig
    if browserstack_config is None:
        browserstack_config = config.BrowserStackConfig
    # Arguments for specifying browser to use
    if browserstack_config.ENABLE:
        browser_choices = list(set(browser_config.BROWSER_TEST_CLASSES) | set(browserstack_config.BROWSER_TEST_CLASSES))
    else:
        browser_choices = list(browser_config.BROWSER_TEST_CLASSES.keys())
    options_help = format_browser_choices(browser_config, browserstack_config)
    parser.add_argument('-b', '--browser', nargs='+', choices=browser_choices, metavar='<browser>',
                        help='Run tests only in the specified browsers.' + options_help)
    # Add argument for running on browserstack if the feature is enabled
    if browserstack_config.ENABLE:
        parser.add_argument('--browserstack', action='store_true',
                            help='Run tests on BrowserStack instead of locally')
    # Arguments for specifying what test to run
    parser.add_argument('-t', '--test', nargs='+', metavar='<test>',
                        help='Run specific test case classes or test methods.\nArguments should be in the format <TestCase>[.<method>]')
    # Arguments for specifying test module to run
    parser.add_argument('-m', '--module', nargs='+', metavar='<module>',
                        help='Run only tests in specific test modules')
    return parser


def format_browser_choices(browser_config, browserstack_config):
    """Format the help string for browser choices

    If BrowserStack is disabled or doesn't have any browsers enabled that aren't also in
    the local browser config, output string will have the following format:

    .. code:: python

        '\\nOptions: {browser0,browser1}'

    If BrowserStack is enabled and there are different browsers enabled for local and
    BrowserStack, output string will have the following format:

    .. code:: python

        '''
        Local & BrowserStack: {browser0,browser1}
        Local Only: {browser2,browser3}
        BrowserStack Only: {browser4,browser5}
        '''

    :param browser_config: BrowserConfig class
    :param browserstack_config: BrowserStackConfig class

    :return: Formatted help string for browser options
    """
    options = ''
    local_set = set(browser_config.BROWSER_TEST_CLASSES)
    browserstack_set = set(browserstack_config.BROWSER_TEST_CLASSES)
    # If browserstack is disabled or there's no difference in browsers
    if not browserstack_config.ENABLE or local_set == browserstack_set:
        options = '\nOptions: ' + browser_list_string(browser_config.BROWSER_TEST_CLASSES)
    # Else if there is some difference between enabled sets
    else:
        both_set = local_set.intersection(browserstack_set)
        local_only = local_set - browserstack_set
        browserstack_only = browserstack_set - local_set
        if both_set:
            options += '\nLocal & BrowserStack: ' + browser_list_string(list(both_set))
        if local_only:
            options += '\nLocal Only: ' + browser_list_string(list(local_only))
        if browserstack_only:
            options += '\nBrowserStack Only: ' + browser_list_string(list(browserstack_only))
    return options


def browser_list_string(browser_names):
    """Takes a list of browser names and returns a string representation in the format
    '{browser0,browser1,browser2}'

    :param browser_names: List of browser names

    :return: String representation of the browser name list
    """
    return '{{{}}}'.format(','.join(browser_names))


def parse_test_names(test_name_args):
    """Returns a dictionary mapping test case names to a list of test functions

    :param test_name_args: The parsed value of the --test command line argument
    :return: None if test_name_args is None, otherwise return a dictionary mapping test
        case names to a list of test functions to run. If list is empty, no specific
        function was given for that class
    """
    if test_name_args is None:
        return None
    class_map = {}
    for test_name in test_name_args:
        test_name_parts = test_name.split('.')
        # If test class name is not yet mapped, map it to an empty list
        if test_name_parts[0] not in class_map.keys():
            class_map[test_name_parts[0]] = []
        # If a function was specified, append it to the list of functions
        if len(test_name_parts) > 1:
            class_map[test_name_parts[0]].append(test_name_parts[1])
    return class_map


def run_tests(tests_module, config_module, browser_classes=None, test_class_map=None, test_module_names=None, browserstack=False):
    """Run tests using parsed args and project modules

    :param tests_module: The module object for <test_project>.tests
    :param config_module: The module object for <test_project>.config or
        webdriver_test_tools.config if not specified
    :param browser_classes: (Optional) List of browser test classes from parsed arg
        for --browser command line argument
    :param test_class_map: (Optional) Result of passing parsed arg for --test command
        line argument to parse_test_names()
    :param test_module_names: (Optional) Parsed arg for --module command line argument
    :param browserstack: (Default = False) If True, generated test cases should run on
        BrowserStack
    """
    # Enable graceful Ctrl+C handling
    unittest.installHandler()
    # Load WebDriverTestCase subclasses from project tests
    test_class_names = None if test_class_map is None else test_class_map.keys()
    tests = test_loader.load_project_tests(tests_module, test_class_names, test_module_names)
    # Generate browser test cases from the loaded WebDriverTestCase classes
    browser_test_suite = test_factory.generate_browser_test_suite(tests, browser_classes, test_class_map, config_module, browserstack)
    # Get configured test runner and run suite
    test_runner = config_module.TestSuiteConfig.get_runner()
    test_runner.run(browser_test_suite)
    # Link to BrowserStack automation dashboard if applicable
    if browserstack:
        # TODO: integrate into custom test runner class
        print('', 'See BrowserStack Automation Dashboard for Detailed Results:',
              'https://www.browserstack.com/automate', sep='\n')



