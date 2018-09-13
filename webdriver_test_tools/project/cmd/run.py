import textwrap
import unittest
from argparse import RawTextHelpFormatter

from webdriver_test_tools import config
from webdriver_test_tools.common import cmd
from webdriver_test_tools.project import test_factory
from webdriver_test_tools.project.cmd.common import parse_test_args, load_tests
from webdriver_test_tools.testcase import Browsers


def add_run_subparser(subparsers, config_module=None, parents=[],
                      formatter_class=RawTextHelpFormatter):
    """Add subparser for the ``<test_package> run`` command

    :param subparsers: ``argparse._SubParsersAction`` object for the test package ArgumentParser (i.e. the object
        returned by the ``add_subparsers()`` method)
    :param config_module: (Optional) The module object for ``<test_project>.config``.
        Will use :mod:`webdriver_test_tools.config` if not specified
        if unspecified
    :param parents: (Default: ``[]``) Parent parsers for the run subparser
    :param formatter_class: (Default: ``argparse.RawTextHelpFormatter``) Class to use for the ``formatter_class``
        parameter

    :return: ``argparse.ArgumentParser`` object for the newly added ``run`` subparser
    """
    # Get browser config classes
    browser_config, browserstack_config = get_browser_config_classes(config_module)
    run_description = 'Run the test suite'
    run_help = run_description
    run_parser = subparsers.add_parser(
        'run', description=run_description, help=run_help,
        parents=parents,  # TODO: always use test_parent_parser?
        formatter_class=formatter_class,
        add_help=False, epilog=cmd.argparse.ARGPARSE_EPILOG
    )
    # Browser Arguments
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
        video_default = True if 'browserstack.video' not in browserstack_config.BS_CAPABILITIES else \
            browserstack_config.BS_CAPABILITIES['browserstack.video']
        run_parser.set_defaults(video=video_default)
    # Output Arguments
    group = run_parser.add_argument_group('Output Options')
    verbosity_help = textwrap.dedent('''\
                             0 - Final results only
                             1 - Final results and progress indicator
                             2 - Full output
                             ''')
    group.add_argument('-v', '--verbosity', type=int, choices=[0, 1, 2],
                       metavar='<level>', help=verbosity_help)
    return run_parser


# Help text formatting functions

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


# Config module helper functions

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


# Argument parsing functions

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
    tests = load_tests(tests_module, test_module_names, test_class_map, skip_class_map)
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
