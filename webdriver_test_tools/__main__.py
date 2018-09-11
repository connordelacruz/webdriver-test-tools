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
    command_desc = 'Run \'{} <command> --help\' for details'.format(parser.prog)
    subparsers = parser.add_subparsers(
        title='Commands', description=command_desc, dest='command', metavar='<command>'
    )
    # init command
    init_description = 'Initialize a new test project in the current directory. \
        If no arguments are provided, a prompt will walk you through project initialization.'
    init_help = init_description
    init_parser = subparsers.add_parser(
        'init', description=init_description, help=init_help,
        epilog=cmd.argparse.ARGPARSE_EPILOG,
        parents=[generic_parent_parser], add_help=False,
    )
    # Positional Arguments
    positional_args = init_parser.add_argument_group('Positional Arguments')
    package_name_help = 'Name for the new test package \
        (alphanumeric characters and underscores only. Cannot start with a number)'
    positional_args.add_argument(
        'package_name', metavar='<package_name>', nargs='?', default=None,
        help=package_name_help
    )
    project_title_help = '(Optional) Friendly name for the test project. \
        Defaults to the value of <package_name> if not provided'
    positional_args.add_argument(
        'project_title', metavar='<"Project Title">', nargs='?', default=None,
        help=project_title_help
    )
    # Optional Arguments
    optional_args_description='Override default behaviour when initializing a project from the command line.'
    optional_args = init_parser.add_argument_group(
        'Options', optional_args_description
    )
    no_gitignore_help = 'Do not create .gitignore files for project root and log directory'
    optional_args.add_argument(
        '--no-gitignore', action='store_false', default=None,
        help=no_gitignore_help
    )
    no_readme_help = 'Do not generate README file with usage info'
    optional_args.add_argument(
        '--no-readme', action='store_false', default=None,
        help=no_readme_help
    )
    return parser


def main():
    """Parse command line arguments and handle appropriately"""
    parser = get_parser()
    args = parser.parse_args()
    if args.version is not None and args.version:
        print('webdriver_test_tools ' + __version__)
        return
    if args.command == 'init':
        initialize.main(
            package_name=args.package_name, project_title=args.project_title,
            gitignore=args.no_gitignore, readme=args.no_readme
        )
    # If no arguments were specified, print help
    else:
        parser.print_help()


if __name__ == '__main__':
    main()

