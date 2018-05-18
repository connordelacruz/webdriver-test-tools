"""Functions for test project ``__main__`` modules"""

import argparse
import unittest
import textwrap

from webdriver_test_tools import cmd, config
from webdriver_test_tools.__about__ import __documentation__
from webdriver_test_tools.testcase import Browsers
from webdriver_test_tools.project import test_loader, test_factory


def main(tests_module, config_module=None, package_name=None):
    """Function to call in test modules ``if __name__ == '__main__'`` at run time

    :param tests_module: The module object for ``<test_project>.tests``
    :param config_module: (Optional) The module object for ``<test_project>.config``.
        Will use :mod:`webdriver_test_tools.config` if not specified
    :param package_name: (Optional) The name of the package (i.e. ``__package__``)
    """
    if config_module is None:
        config_module = config
    browser_config = config_module.BrowserConfig
    # Older projects may not have the BrowserStackConfig class
    browserstack_config = config_module.BrowserStackConfig if 'BrowserStackConfig' in dir(config_module) else config.BrowserStackConfig
    # Parse arguments
    args = get_parser(browser_config, browserstack_config, package_name).parse_args()
    # get --test, --skip, and --module args
    kwargs = {
        'test_class_map': parse_test_names(args.test),
        'skip_class_map': parse_test_names(args.skip),
        'test_module_names': args.module,
    }
    # If --list is specified, print available tests and exit
    if args.list:
        list_tests(tests_module, **kwargs)
        exit()
    # Parse --browserstack, --headless, and --verbosity args
    kwargs.update({
        'browserstack': 'browserstack' in dir(args) and args.browserstack,
        'headless': args.headless,
        'verbosity': args.verbosity,
    })
    # Handle --browser args
    browser_config_class = browserstack_config if kwargs['browserstack'] else browser_config
    kwargs['browser_classes'] = browser_config_class.get_browser_classes(args.browser)
    # Run tests using parsed args
    run_tests(tests_module, config_module, **kwargs)


def get_parser(browser_config=None, browserstack_config=None, package_name=None):
    """Returns the ``ArgumentParser`` object for use with ``main()``

    :param browser_config: (Optional) ``BrowserConfig`` class for the project. Defaults to
        :class:`webdriver_test_tools.config.BrowserConfig
        <webdriver_test_tools.config.browser.BrowserConfig>`
        if unspecified
    :param browserstack_config: (Optional) ``BrowserStackConfig`` class for the project.
        Defaults to
        :class:`webdriver_test_tools.config.BrowserStackConfig
        <webdriver_test_tools.config.browser.BrowserStackConfig>`
        if unspecified
    :param package_name: (Optional) The name of the package (i.e. ``__package__``)

    :return: ``ArgumentParser`` for the test package
    """
    description = 'Run the test suite.'
    epilog = 'For more information, visit <{}>'.format(__documentation__)
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, add_help=False,
                                     prog=package_name, description=description, epilog=epilog)
    # Use default config if module is None or doesn't contain BrowserConfig class
    if browser_config is None:
        browser_config = config.BrowserConfig
    if browserstack_config is None:
        browserstack_config = config.BrowserStackConfig
    # Arguments for specifying what test to run
    group = parser.add_argument_group('Test Arguments')
    module_help = 'Run only tests in specific test modules'
    group.add_argument('-m', '--module', nargs='+', metavar='<module>', help=module_help)
    test_help = textwrap.dedent('''\
                Run specific test case classes or test methods.
                Arguments should be in the format <TestCase>[.<method>]
                ''')
    group.add_argument('-t', '--test', nargs='+', metavar='<test>', help=test_help)
    skip_help = textwrap.dedent('''\
                Skip specific test case classes or test methods.
                Arguments should be in the format <TestCase>[.<method>]
                ''')
    group.add_argument('-s', '--skip', nargs='+', metavar='<test>', help=skip_help)
    # Arguments for specifying browser to use
    group = parser.add_argument_group('Browser Arguments')
    if browserstack_config.ENABLE:
        browser_choices = list(set(browser_config.get_browser_names()) | set(browserstack_config.get_browser_names()))
    else:
        browser_choices = list(browser_config.get_browser_names())
    browser_options_help = _format_browser_choices(browser_config, browserstack_config)
    browser_help = 'Run tests only in the specified browsers.' + browser_options_help
    group.add_argument('-b', '--browser', nargs='+', choices=browser_choices, metavar='<browser>',
                       help=browser_help)
    headless_options_help = _format_headless_browsers(browser_config)
    headless_help = 'Run tests using headless browsers.' + headless_options_help
    group.add_argument('-H', '--headless', action='store_true', help=headless_help)
    if browserstack_config.ENABLE:
        browserstack_help = 'Run tests on BrowserStack instead of locally'
        group.add_argument('-B', '--browserstack', action='store_true', help=browserstack_help)
    # Output arguments
    group = parser.add_argument_group('Output Options')
    verbosity_help = textwrap.dedent('''\
                             0 - Final results only
                             1 - Final results and progress indicator
                             2 - Full output
                             ''')
    group.add_argument('-v', '--verbosity', type=int, choices=[0, 1, 2],
                       metavar='<level>', help=verbosity_help)
    # Command arguments
    group = parser.add_argument_group('Commands')
    help_help = 'Show this help message and exit'
    group.add_argument('-h', '--help', action='help', help=help_help)
    list_help = 'Print a list of available tests and exit'
    group.add_argument('-l', '--list', action='store_true', help=list_help)
    return parser


def _format_browser_choices(browser_config, browserstack_config):
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
    local_set = set(browser_config.get_browser_names())
    browserstack_set = set(browserstack_config.get_browser_names())
    # If browserstack is disabled or there's no difference in browsers
    if not browserstack_config.ENABLE or local_set == browserstack_set:
        options = '\nOptions: ' + _browser_list_string(browser_config.get_browser_names())
    # Else if there is some difference between enabled sets
    else:
        both_set = local_set.intersection(browserstack_set)
        local_only = local_set - browserstack_set
        browserstack_only = browserstack_set - local_set
        if both_set:
            options += '\nLocal & BrowserStack:\n' + cmd.INDENT + _browser_list_string(list(both_set))
        if local_only:
            options += '\nLocal Only:\n' + cmd.INDENT + _browser_list_string(list(local_only))
        if browserstack_only:
            options += '\nBrowserStack Only:\n' + cmd.INDENT + _browser_list_string(list(browserstack_only))
    return options


def _format_headless_browsers(browser_config):
    """Format the help string for compatible browsers in ``--headless`` argument help string

    :param browser_config: :class:`BrowserConfig <webdriver_test_tools.config.browser.BrowserConfig>` class

    :return: Formatted help string for browser options
    """
    enabled_browsers = browser_config.get_browser_names()
    browser_names = [
        browser_class.SHORT_NAME for browser_class in Browsers.HEADLESS_COMPATIBLE
        if browser_class.SHORT_NAME in enabled_browsers
    ]
    return '\nCompatible Browsers:\n' + cmd.INDENT + _browser_list_string(browser_names)


def _browser_list_string(browser_names):
    """Takes a list of browser names and returns a string representation in the format
    '{browser0,browser1,browser2}'

    :param browser_names: List of browser names

    :return: String representation of the browser name list
    """
    return '{{{}}}'.format(','.join(browser_names))


def parse_test_names(test_name_args):
    """Returns a dictionary mapping test case names to a list of test functions

    :param test_name_args: The parsed value of the ``--test`` or ``--skip`` arguments

    :return: None if ``test_name_args`` is None, otherwise return a dictionary mapping test
        case names to a list of test functions to run. If list is empty, no specific
        function was given for that class
    """
    if test_name_args is None:
        return None
    class_map = {}
    for test_name in test_name_args:
        test_name_parts = test_name.split('.')
        class_map.setdefault(test_name_parts[0], [])
        # If a function was specified, append it to the list of functions
        if len(test_name_parts) > 1:
            class_map[test_name_parts[0]].append(test_name_parts[1])
    return class_map


def list_tests(tests_module,
               test_module_names=None, test_class_map=None, skip_class_map=None):
    """Print a list of available tests

    :param tests_module: The module object for ``<test_project>.tests``
    :param test_module_names: (Optional) Parsed arg for ``--module`` command line
        argument
    :param test_class_map: (Optional) Result of passing parsed arg for ``--test``
        command line argument to :func:`parse_test_names()`
    :param skip_class_map: (Optional) Result of passing parsed arg for ``--skip``
        command line argument to :func:`parse_test_names()`
    """
    tests = _load_tests(tests_module, test_module_names, test_class_map, skip_class_map)
    for test_class in tests:
        print(cmd.COLORS['title'](test_class.__name__) + ':')
        test_cases = unittest.loader.getTestCaseNames(test_class, 'test')
        for test_case in test_cases:
            print(textwrap.indent(test_case, cmd.INDENT))


def run_tests(tests_module, config_module, browser_classes=None,
              test_class_map=None, skip_class_map=None, test_module_names=None,
              browserstack=False, headless=False, verbosity=None):
    """Run tests using parsed args and project modules

    :param tests_module: The module object for ``<test_project>.tests``
    :param config_module: The module object for ``<test_project>.config`` or
        :mod:`webdriver_test_tools.config` if not specified
    :param browser_classes: (Optional) List of browser test classes from parsed arg
        for ``--browser`` command line argument
    :param test_class_map: (Optional) Result of passing parsed arg for ``--test``
        command line argument to :func:`parse_test_names()`
    :param skip_class_map: (Optional) Result of passing parsed arg for ``--skip``
        command line argument to :func:`parse_test_names()`
    :param test_module_names: (Optional) Parsed arg for ``--module`` command line
        argument
    :param browserstack: (Default = False) If True, generated test cases should run on
        BrowserStack
    :param headless: (Default = False) If True, configure driver to run tests in a
        headless browser. Tests will only be generated for drivers that support
        running headless browsers
    :param verbosity: (Optional) Output verbosity level for the test runner.
    """
    # Enable graceful Ctrl+C handling
    unittest.installHandler()
    # Load WebDriverTestCase subclasses from project tests
    tests = _load_tests(tests_module, test_module_names, test_class_map, skip_class_map)
    # Generate browser test cases from the loaded WebDriverTestCase classes
    browser_test_suite = test_factory.generate_browser_test_suite(
        tests, browser_classes, test_class_map, skip_class_map,
        config_module, browserstack, headless
    )
    # Get configured test runner and run suite
    test_runner = config_module.TestSuiteConfig.get_runner(verbosity=verbosity)
    test_runner.run(browser_test_suite)
    # Link to BrowserStack automation dashboard if applicable
    if browserstack:
        print('', 'See BrowserStack Automation Dashboard for Detailed Results:',
              'https://www.browserstack.com/automate', sep='\n')


def _load_tests(tests_module, test_module_names=None, test_class_map=None, skip_class_map=None):
    """Return a list of test classes from a project based on the --module, --test, and --skip arguments

    :param tests_module: The module object for <test_project>.tests
    :param test_module_names: (Optional) Parsed arg for --module command line argument
    :param test_class_map: (Optional) Result of passing parsed arg for --test command
        line argument to parse_test_names()
    :param skip_class_map: (Optional) Result of passing parsed arg for --skip command
        line argument to parse_test_names()

    :return: List of test classes
    """
    test_class_names = None if test_class_map is None else test_class_map.keys()
    skip_class_names = _get_skip_class_names(skip_class_map)
    return test_loader.load_project_tests(tests_module, test_module_names, test_class_names, skip_class_names)


def _get_skip_class_names(skip_class_map):
    """Returns list of classes to skip

    Returned list only contains names of classes where all methods are skipped.
    If skip_class_map is None, returns None

    :param skip_class_map: Result of passing parsed arg for --skip command line argument to parse_test_names()
    """
    if skip_class_map:
        return [
            class_name for class_name, methods in skip_class_map.items() if not methods
        ]
    return None

