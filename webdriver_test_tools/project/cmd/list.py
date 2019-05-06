import textwrap
import unittest
from argparse import RawTextHelpFormatter

from webdriver_test_tools.common import cmd
from webdriver_test_tools.project.cmd.common import parse_test_args, load_tests


def add_list_subparser(subparsers, parents=[],
                       formatter_class=RawTextHelpFormatter):
    """Add subparser for the ``<test_package> list`` command

    :param subparsers: ``argparse._SubParsersAction`` object for the test
        package ArgumentParser (i.e. the object returned by the
        ``add_subparsers()`` method)
    :param parents: (Default: ``[]``) Parent parsers for the list subparser
    :param formatter_class: (Default: ``argparse.RawTextHelpFormatter``) Class
        to use for the ``formatter_class`` parameter

    :return: ``argparse.ArgumentParser`` object for the newly added ``list``
        subparser
    """
    list_description = 'Print a list of available tests and exit'
    list_help = list_description
    list_parser = subparsers.add_parser(
        'list', description=list_description, help=list_help,
        parents=parents,  # TODO: always use test_parent_parser?
        formatter_class=formatter_class,
        add_help=False, epilog=cmd.argparse.ARGPARSE_EPILOG
    )
    # Output Arguments
    group = list_parser.add_argument_group('Output Options')
    # TODO: better help?
    verbose_help = 'Show class and method docstrings'
    group.add_argument('-v', '--verbose', action='store_true', default=False,
                       help=verbose_help)
    return list_parser


# Argument parsing functions

def parse_list_args(tests_module, args):
    """Parse arguments and run the 'list' command

    :param tests_module: The module object for ``<test_project>.tests``
    :param args: The namespace returned by parser.parse_args()
    """
    kwargs = parse_test_args(args)
    kwargs['verbose'] = args.verbose
    list_tests(tests_module, **kwargs)


def list_tests(tests_module,
               test_module_names=None, test_class_map=None, skip_class_map=None,
               verbose=False):
    """Print a list of available tests

    :param tests_module: The module object for ``<test_project>.tests``
    :param test_module_names: (Optional) Parsed arg for ``--module`` command
        line argument
    :param test_class_map: (Optional) Result of passing parsed arg for
        ``--test`` command line argument to :func:`parse_test_names()`
    :param skip_class_map: (Optional) Result of passing parsed arg for
        ``--skip`` command line argument to :func:`parse_test_names()`
    :param verbose: (Default = False) If True, print class and test method
        docstrings
    """
    tests = load_tests(tests_module, test_module_names, test_class_map, skip_class_map)
    module_map = _module_map(tests, tests_module)
    for module, test_list in module_map.items():
        _print_module(module, test_list, verbose=verbose)


def _module_map(tests, tests_module):
    """Returns a dictionary mapping test module names to a list of the test
    case classes in the module

    :param tests: List of test case classes
    :param tests_module: The module object for ``<test_project>.tests``

    :return: Dictionary mapping test module names to a list of the test
        case classes in the module
    """
    module_prefix = tests_module.__name__ + '.'
    module_map = {}
    for test in tests:
        module = test.__module__.replace(module_prefix, '')
        if module not in module_map:
            module_map[module] = []
        module_map[module].append(test)
    return module_map


def _print_module(module, test_list, verbose=False):
    """Print a test module

    :param module: The name of the test module to print
    :param test_list: The list of test classes in the module to print
    :param verbose: (Default = False) If True, print class and test method
        docstrings
    """
    print(cmd.COLORS['prompt'](module) + ':')
    for test_class in test_list:
        _print_test_case(test_class, verbose=verbose)


def _print_test_case(test_class, verbose=False, indent=cmd.INDENT):
    """Print a test case class

    :param test_class: The test case class to print
    :param verbose: (Default = False) If True, print class and test method
        docstrings
    :param indent: (Default = :const:`cmd.INDENT
        <webdriver_test_tools.common.cmd.cmd.INDENT>`) The string to use for
        indentation when printing the class
    """
    print(textwrap.indent(cmd.COLORS['title'](test_class.__name__) + ':', indent))
    if verbose and hasattr(test_class, '__doc__'):
        cmd.print_shortened(test_class.__doc__, indent=indent, fmt='info')
    methods = unittest.loader.getTestCaseNames(test_class, 'test')
    for method in methods:
        _print_method(method, test_class=test_class, verbose=verbose)


def _print_method(method, test_class, verbose=False, indent=cmd.INDENT*2):
    """Print a test method

    :param method: The name of the method to print
    :param test_class: The test case class containing the method to print
    :param verbose: (Default = False) If True, print test method docstrings
    :param indent: (Default = :const:`cmd.INDENT
        <webdriver_test_tools.common.cmd.cmd.INDENT>` * 2) The string to use
        for indentation when printing the class
    """
    print(textwrap.indent(method, indent))
    if verbose:
        # TODO: catch attribute error
        func = getattr(test_class, method)
        if hasattr(func, '__doc__'):
            cmd.print_shortened(func.__doc__, indent=indent, fmt='info')

