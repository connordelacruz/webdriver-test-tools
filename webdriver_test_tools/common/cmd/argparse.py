"""Extended ArgumentParser class and common argparse utilities"""
import argparse
import sys

from webdriver_test_tools.__about__ import __documentation__


# Extended ArgumentParser class

class ArgumentParser(argparse.ArgumentParser):
    """Extended ArgumentParser class with support for default subparser"""

    def set_default_subparser(self, name, subcommand_arg_position=1):
        """default subparser selection. Call after setup, just before parse_args()

        :param name: is the name of the subparser to call by default
        :param subcommand_arg_position: (Default: 1) The position where
            subcommand arguments should be. 0 is the name of the module being
            run, so should be > 0

        Based on: https://stackoverflow.com/a/26379693
        """
        subparser_found = False
        for arg in sys.argv[1:]:
            if arg in ['-h', '--help']:  # global help if no subparser
                break
        else:
            for x in self._subparsers._actions:
                if not isinstance(x, argparse._SubParsersAction):
                    continue
                for sp_name in x._name_parser_map.keys():
                    if sp_name in sys.argv[1:]:
                        subparser_found = True
            if not subparser_found:
                # insert default in position specified by subcommand_arg_position
                sys.argv.insert(subcommand_arg_position, name)


# Common argparse items

#: Generic "for more information" argument parser epilog
ARGPARSE_EPILOG = 'For more information, visit <{}>'.format(__documentation__)


def get_generic_parent_parser(include_version=False):
    """Returns a generic :class:`ArgumentParser
    <webdriver_test_tools.cmd.argparse.ArgumentParser>` with ``--help`` and
    (optionally) ``--version`` arguments

    :param include_version: (Default: False) If True, include ``--version``
        argument

    :return: Generic :class:`ArgumentParser
        <webdriver_test_tools.cmd.argparse.ArgumentParser>` with a 'General'
        argument group with ``--help`` and (optionally) ``--version`` arguments
    """
    generic_parent_parser = ArgumentParser(add_help=False)
    group = generic_parent_parser.add_argument_group('General')
    group.add_argument('-h', '--help', action='help',
                       help='Show this help message and exit')
    if include_version:
        group.add_argument('-V', '--version', action='store_true',
                           help='Show version number and exit')
    return generic_parent_parser


