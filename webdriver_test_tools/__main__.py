#!/usr/bin/env python3
"""webdriver_test_tools command line interface"""
from webdriver_test_tools.cmd import init, version
from webdriver_test_tools.common import cmd


def get_parser():
    """Returns ``ArgumentParser`` object for use with :func:`main()`"""
    generic_parent_parser = cmd.argparse.get_generic_parent_parser(include_version=True)
    wtt_description = 'Aliases: webdriver_test_tools, wtt'
    parser = cmd.argparse.ArgumentParser(
        description=wtt_description, epilog=cmd.argparse.ARGPARSE_EPILOG,
        parents=[generic_parent_parser], add_help=False
    )
    # Subparsers
    command_desc = 'Run \'{} <command> --help\' for details'.format(parser.prog)
    subparsers = parser.add_subparsers(
        title='Commands', description=command_desc, dest='command', metavar='<command>'
    )
    init_parser = init.add_init_subparser(subparsers, parents=[generic_parent_parser])
    return parser


def main():
    """Parse command line arguments and handle appropriately"""
    parser = get_parser()
    args = parser.parse_args()
    if args.version is not None and args.version:
        version.main()
    elif args.command == 'init':
        init.main(args)
    # If no arguments were specified, print help
    else:
        parser.print_help()


if __name__ == '__main__':
    main()

