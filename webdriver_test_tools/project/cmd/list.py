import textwrap
import unittest
from argparse import RawTextHelpFormatter

from webdriver_test_tools.common import cmd
from webdriver_test_tools.project.cmd.common import parse_test_args, load_tests


def add_list_subparser(subparsers, parents=[],
                       formatter_class=RawTextHelpFormatter):
    """Add subparser for the ``<test_package> list`` command

    :param subparsers: ``argparse._SubParsersAction`` object for the test package ArgumentParser (i.e. the object
        returned by the ``add_subparsers()`` method)
    :param parents: (Default: ``[]``) Parent parsers for the list subparser
    :param formatter_class: (Default: ``argparse.RawTextHelpFormatter``) Class to use for the ``formatter_class``
        parameter

    :return: ``argparse.ArgumentParser`` object for the newly added ``list`` subparser
    """
    list_description = 'Print a list of available tests and exit'
    list_help = list_description
    # TODO: aliases=['ls']
    list_parser = subparsers.add_parser(
        'list', description=list_description, help=list_help,
        parents=parents,  # TODO: always use test_parent_parser?
        formatter_class=formatter_class,
        add_help=False, epilog=cmd.argparse.ARGPARSE_EPILOG
    )
    return list_parser


# Argument parsing functions

def parse_list_args(tests_module, args):
    """Parse arguments and run the 'list' command

    :param tests_module: The module object for ``<test_project>.tests``
    :param args: The namespace returned by parser.parse_args()
    """
    kwargs = parse_test_args(args)
    list_tests(tests_module, **kwargs)


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
    tests = load_tests(tests_module, test_module_names, test_class_map, skip_class_map)
    for test_class in tests:
        print(cmd.COLORS['title'](test_class.__name__) + ':')
        test_cases = unittest.loader.getTestCaseNames(test_class, 'test')
        for test_case in test_cases:
            print(textwrap.indent(test_case, cmd.INDENT))
