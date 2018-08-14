"""Functions for test project ``__main__`` modules"""

import argparse
import unittest
import textwrap
import os

from webdriver_test_tools import cmd, config
from webdriver_test_tools.testcase import Browsers
from webdriver_test_tools.project import test_loader, test_factory
from webdriver_test_tools.project.new_file import new_file


def main(tests_module, config_module=None, package_name=None):
    """Function to call in test modules ``if __name__ == '__main__'`` at run time

    :param tests_module: The module object for ``<test_project>.tests``
    :param config_module: (Optional) The module object for ``<test_project>.config``.
        Will use :mod:`webdriver_test_tools.config` if not specified
    :param package_name: (Optional) The name of the package (i.e. ``__package__``)
    """
    # Parse arguments
    parser = get_parser(config_module, package_name)
    # Set run as the default command parser
    parser.set_default_subparser('run')
    args = parser.parse_args()
    if args.command == 'list':
        parse_list_args(tests_module, args)
    elif args.command == 'new':
        parse_new_args(package_name, tests_module, args)
    elif args.command == 'run' or args.command is None:
        parse_run_args(tests_module, config_module, args)
    else:
        parser.print_help()


# Argument parser

def get_parser(config_module=None, package_name=None):
    """Returns the ``ArgumentParser`` object for use with ``main()``

    :param config_module: (Optional) The module object for ``<test_project>.config``.
        Will use :mod:`webdriver_test_tools.config` if not specified
        if unspecified
    :param package_name: (Optional) The name of the package (i.e. ``__package__``)

    :return: ``ArgumentParser`` for the test package
    """
    if package_name is None:
        package_name = '<test_package>'
    # Parent parsers
    # Adds custom --help argument
    generic_parent_parser = cmd.argparse.get_generic_parent_parser()
    # Adds --module, --test, and --skip arguments
    test_parent_parser = get_test_parent_parser(parents=[generic_parent_parser])

    # Top level parser
    parser = cmd.argparse.ArgumentParser(
        parents=[generic_parent_parser],
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False, prog=package_name, epilog=cmd.argparse.ARGPARSE_EPILOG
    )
    # Get browser config classes
    browser_config, browserstack_config = get_browser_config_classes(config_module)

    # Subparsers
    command_desc = 'Run \'{} <command> --help\' for details'.format(package_name)
    subparsers = parser.add_subparsers(
        title='Commands', description=command_desc, dest='command', metavar='<command>'
    )

    # Run command
    run_description = 'Run the test suite'
    run_help = run_description
    run_parser = subparsers.add_parser(
        'run', description=run_description, help=run_help,
        parents=[test_parent_parser],
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False, epilog=cmd.argparse.ARGPARSE_EPILOG
    )
    # Arguments for specifying browser to use
    group = run_parser.add_argument_group('Browser Arguments')
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
    # BrowserStack arguments
    if browserstack_config.ENABLE:
        group = run_parser.add_argument_group('BrowserStack')
        browserstack_help = 'Run tests on BrowserStack instead of locally'
        group.add_argument('-B', '--browserstack', action='store_true', help=browserstack_help)
        # Build name
        build_help = 'Set the build name for the group of tests'
        group.add_argument('--build', metavar='<name>', help=build_help)
        # Enabling/disabling video recording
        video_help = 'Record video of tests'
        group.add_argument('--video', dest='video', action='store_true', help=video_help)
        no_video_help = 'Disable video recording'
        group.add_argument('--no-video', dest='video', action='store_false', help=no_video_help)
        # Set default to the value configured in browserstack_config (or True if not configured)
        # TODO: move to BrowserStackConfig class method?
        video_default = True if 'browserstack.video' not in browserstack_config.BS_CAPABILITIES else browserstack_config.BS_CAPABILITIES['browserstack.video']
        run_parser.set_defaults(video=video_default)
    # Output arguments
    group = run_parser.add_argument_group('Output Options')
    verbosity_help = textwrap.dedent('''\
                             0 - Final results only
                             1 - Final results and progress indicator
                             2 - Full output
                             ''')
    group.add_argument('-v', '--verbosity', type=int, choices=[0, 1, 2],
                       metavar='<level>', help=verbosity_help)

    # List command
    list_description = 'Print a list of available tests and exit'
    list_help = list_description
    list_parser = subparsers.add_parser(
        'list', description=list_description, help=list_help,
        parents=[test_parent_parser],
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False, epilog=cmd.argparse.ARGPARSE_EPILOG
    )

    # New command
    new_description = 'Create a new test module or page object'
    new_help = new_description
    new_parser = subparsers.add_parser(
        'new', description=new_description, help=new_help,
        parents=[generic_parent_parser],
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False, epilog=cmd.argparse.ARGPARSE_EPILOG
    )
    # New <type> subparsers
    new_type_desc = 'Run \'{} new <type> --help\' for details'.format(package_name)
    new_subparsers = new_parser.add_subparsers(
        title='File Types', description=new_type_desc, dest='type', metavar='<type>'
    )
    # New test parser
    new_test_parent_parser = get_new_parent_parser(
        parents=[generic_parent_parser], class_name_metavar='<TestCaseClass>',
        class_name_help='Name to use for the initial test case class'
    )
    new_test_description='Create a new test module'
    new_test_help=new_test_description
    new_subparsers.add_parser(
        'test', description=new_test_description, help=new_test_help,
        parents=[new_test_parent_parser],
        add_help=False, epilog=cmd.argparse.ARGPARSE_EPILOG
    )
    # New page object parser
    new_page_parent_parser = get_new_parent_parser(
        parents=[generic_parent_parser], class_name_metavar='<PageObjectClass>',
        class_name_help='Name to use for the initial page object class'
    )
    new_page_description='Create a new page object module'
    new_page_help=new_page_description
    new_page_parser = new_subparsers.add_parser(
        'page', description=new_page_description, help=new_page_help,
        parents=[new_page_parent_parser],
        add_help=False, epilog=cmd.argparse.ARGPARSE_EPILOG
    )
    # TODO: add optional --prototype arg with a list of valid page object prototype classes

    return parser


def get_test_parent_parser(parents=[]):
    """Returns an :class:`ArgumentParser
    <webdriver_test_tools.cmd.argparse.ArgumentParser>` with ``--test``,
    ``--skip``, and ``--module`` arguments

    :param parents: (Optional) List of ``ArgumentParser`` objects to use as
        parents for the test argument parser

    :return: :class:`ArgumentParser
        <webdriver_test_tools.cmd.argparse.ArgumentParser>` with ``--test``,
        ``--skip``, and ``--module`` arguments
    """
    # Adds --module, --test, and --skip arguments
    test_parent_parser = cmd.argparse.ArgumentParser(add_help=False, parents=parents)
    # Arguments for specifying what test to run
    group = test_parent_parser.add_argument_group('Test Arguments')
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
    return test_parent_parser


def get_new_parent_parser(parents=[], class_name_metavar='<ClassName>',
                          class_name_help='Name to use for the initial class'):
    """Returns an :class:`ArgumentParser
    <webdriver_test_tools.cmd.argparse.ArgumentParser>` with ``<module_name>``,
    ``<class_name>``, and ``--description`` arguments

    :param parents: (Optional) List of ``ArgumentParser`` objects to use as
        parents for the test argument parser
    :param class_name_metavar: (Optional) Metavar to display for the class_name
        argument
    :param class_name_help: (Optional) Help text to use for the class_name
        argument

    :return: :class:`ArgumentParser
        <webdriver_test_tools.cmd.argparse.ArgumentParser>` with
        ``<module_name>``, ``<class_name>``, and ``--description`` arguments
    """
    new_parent_parser = cmd.argparse.ArgumentParser(add_help=False, parents=parents)
    # Positional arguments
    module_name_help = 'Filename to use for the new python module'
    new_parent_parser.add_argument('module_name', metavar='<module_name>',
                                   help=module_name_help)
    new_parent_parser.add_argument('class_name', metavar=class_name_metavar,
                                   help=class_name_help)
    # Optional arguments
    description_help='Description for the initial class'
    new_parent_parser.add_argument('-d', '--description', metavar='<description>',
                                   help=description_help)
    force_help='Force overwrite if a file with the same name already exists'
    new_parent_parser.add_argument('-f', '--force', action='store_true', default=False,
                                   help=force_help)

    return new_parent_parser


# Help text output functions

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


# Command line argument parsing functions

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


def parse_test_args(args):
    """Parse optional arguments for specifying/skipping tests and modules

    :param args: The namespace returned by parser.parse_args()

    :return: A dictionary mapping 'test_class_map', 'skip_class_map', and
        'test_module_names' to the arguments passed via the command line
    """
    # get --test, --skip, and --module args
    return {
        'test_class_map': parse_test_names(args.test),
        'skip_class_map': parse_test_names(args.skip),
        'test_module_names': args.module,
    }


def parse_list_args(tests_module, args):
    """Parse arguments and run the 'list' command

    :param tests_module: The module object for ``<test_project>.tests``
    :param args: The namespace returned by parser.parse_args()
    """
    kwargs = parse_test_args(args)
    list_tests(tests_module, **kwargs)


def parse_run_args(tests_module, config_module, args):
    """Parse arguments and run the 'run' command

    :param tests_module: The module object for ``<test_project>.tests``
    :param config_module: The module object for ``<test_project>.config``
    :param args: The namespace returned by parser.parse_args()
    """
    kwargs = parse_test_args(args)
    # Get browser config classes
    browser_config, browserstack_config = get_browser_config_classes(config_module)
    # Parse browserstack args
    if 'browserstack' in dir(args):
        kwargs['browserstack'] = args.browserstack
        # Update browserstack_config attributes based on CLI overrides
        if args.browserstack:
            browserstack_config.update_configurations(build=args.build, video=args.video)
    # Parse --headless and --verbosity args
    kwargs.update({
        'headless': args.headless,
        'verbosity': args.verbosity,
    })
    # Handle --browser args
    browser_config_class = browserstack_config if 'browserstack' in kwargs and kwargs['browserstack'] else browser_config
    kwargs['browser_classes'] = browser_config_class.get_browser_classes(args.browser)
    # Run tests using parsed args
    run_tests(tests_module, config_module, **kwargs)


def parse_new_args(package_name, tests_module, args):
    """Parse arguments and run the 'new' command

    :param package_name: Name of the test package
    :param tests_module: The module object for ``<test_project>.tests``. Used
        to determine the filepath of the package
    :param args: The namespace returned by parser.parse_args()
    """
    # Get package path based on tests_module path
    test_package_path = os.path.dirname(os.path.dirname(tests_module.__file__))
    try:
        new_file(test_package_path, package_name, args.type, args.module_name, args.class_name,
                 description=args.description, force=args.force)
    except Exception as e:
        print('')
        cmd.print_exception(e)


def get_browser_config_classes(config_module):
    """Get the ``BrowserConfig`` and ``BrowserStackConfig`` classes from a project.

    :param config_module: The module object for ``<test_project>.config``

    :return: Tuple containing:

        - ``config_module.BrowserConfig`` (or
          :class:`webdriver_test_tools.config.BrowserConfig
          <webdriver_test_tools.config.browser.BrowserConfig>` if not present in
          ``config_module``)
        - ``config_module.BrowserStackConfig`` (or
          :class:`webdriver_test_tools.config.BrowserStackConfig
          <webdriver_test_tools.config.browser.BrowserStackConfig>` if not
          present in ``config_module``)
    """
    if config_module is None:
        config_module = config
    # TODO: set config_module.<Class> instead so this only needs to be called once?
    # All projects should have a BrowserConfig class, but just in case
    browser_config = config_module.BrowserConfig if 'BrowserConfig' in dir(config_module) else config.BrowserConfig
    # Older projects may not have the BrowserStackConfig class
    browserstack_config = config_module.BrowserStackConfig if 'BrowserStackConfig' in dir(config_module) else config.BrowserStackConfig
    return browser_config, browserstack_config


# Sub-command functions

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


def run_tests(tests_module, config_module,
              browser_classes=None, test_class_map=None, skip_class_map=None,
              test_module_names=None, browserstack=False, headless=False,
              verbosity=None):
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
              'https://automate.browserstack.com', sep='\n')


# Test loading functions

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

