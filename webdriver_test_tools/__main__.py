#!/usr/bin/env python3
"""webdriver_test_tools command line interface"""

import argparse

from webdriver_test_tools import cmd
from webdriver_test_tools.__about__ import __version__, __documentation__
from webdriver_test_tools.project import initialize


def get_parser():
    """Returns ``ArgumentParser`` object for use with :func:`main()`"""
    generic_parent_parser = cmd.argparse.get_generic_parent_parser(include_version=True)
    wtt_description = 'Aliases: webdriver_test_tools, wtt'
    parser = argparse.ArgumentParser(
        description=wtt_description, epilog=cmd.argparse.ARGPARSE_EPILOG,
        parents=[generic_parent_parser], add_help=False
    )
    subparsers = parser.add_subparsers(
        title='Commands', dest='command', metavar='<command>'
    )
    # init command
    init_description = 'Initialize a new test project in the current directory'
    init_help = init_description
    init_parser = subparsers.add_parser(
        'init', description=init_description, help=init_help,
        epilog=cmd.argparse.ARGPARSE_EPILOG,
        parents=[generic_parent_parser], add_help=False,
    )
    # TODO: add init_parser arguments for the stuff used in init prompt
    return parser


def main():
    """Parse command line arguments and handle appropriately"""
    parser = get_parser()
    args = parser.parse_args()
    if args.version is not None and args.version:
        print('webdriver_test_tools ' + __version__)
        return
    if args.command == 'init':
        initialize.main()
    # If no arguments were specified, print help
    else:
        parser.print_help()


if __name__ == '__main__':
    main()

