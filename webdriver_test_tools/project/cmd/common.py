import sys
import textwrap

from webdriver_test_tools.common import cmd
from webdriver_test_tools.project import test_loader


# Parent Parsers

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
    test_parent_parser = cmd.argparse.ArgumentParser(add_help=False,
                                                     parents=parents)
    # Arguments for specifying what test to run
    group = test_parent_parser.add_argument_group('Test Arguments')
    module_help = 'Run only tests in specific test modules'
    group.add_argument('-m', '--module', nargs='+', metavar='<module>',
                       help=module_help)
    test_help = textwrap.dedent('''\
                Run specific test case classes or test methods.
                Arguments should be in the format <TestCase>[.<method>]
                (Supports wildcards in class and method names)
                ''')
    group.add_argument('-t', '--test', nargs='+', metavar='<test>',
                       help=test_help)
    skip_help = textwrap.dedent('''\
                Skip specific test case classes or test methods.
                Arguments should be in the format <TestCase>[.<method>]
                (Supports wildcards in class and method names)
                ''')
    group.add_argument('-s', '--skip', nargs='+', metavar='<test>',
                       help=skip_help)
    return test_parent_parser


# Test Parsing Functions

def parse_test_names(test_name_args):
    """Returns a dictionary mapping test case names to a list of test functions

    :param test_name_args: The parsed value of the ``--test`` or ``--skip``
        arguments

    :return: None if ``test_name_args`` is None, otherwise return a dictionary
        mapping test case names to a list of test functions to run. If list is
        empty, no specific function was given for that class
    """
    if test_name_args is None:
        return None
    class_map = {}
    for test_name in test_name_args:
        # Split <module>.[<function>]
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


# Test Loading Functions

def load_tests(tests_module, test_module_names=None, test_class_map=None, skip_class_map=None):
    """Return a list of test classes from a project based on the --module,
    --test, and --skip arguments

    If a :exc:`TestCasesNotFoundException
    <webdriver_test_tools.projects.test_loader.TestCasesNotFoundException>` is
    raised when trying to load tests, the error message will be printed and
    :func:`sys.exit` will be called, ending execution

    :param tests_module: The module object for <test_project>.tests
    :param test_module_names: (Optional) Parsed arg for --module command line
        argument
    :param test_class_map: (Optional) Result of passing parsed arg for --test
        command line argument to parse_test_names()
    :param skip_class_map: (Optional) Result of passing parsed arg for --skip
        command line argument to parse_test_names()

    :return: List of test classes
    """
    try:
        return test_loader.load_project_tests(
            tests_module, test_module_names, test_class_map, skip_class_map
        )
    except test_loader.TestCasesNotFoundException as e:
        print('')
        cmd.print_exception(e)
        sys.exit()


