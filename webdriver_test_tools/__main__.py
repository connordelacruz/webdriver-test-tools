#!/usr/bin/env python3
import argparse

from webdriver_test_tools import version
from webdriver_test_tools.project import initialize


def get_parser():
    """Returns ArgumentParser object for use with main()"""
    parser = argparse.ArgumentParser(add_help=False, epilog='For more information, visit <http://connordelacruz.com/webdriver-test-tools/>')
    group = parser.add_argument_group('Commands')
    # Argument for initializing
    group.add_argument('-i', '--init', action='store_true',
                       help='Initialize a new test project in the current directory')
    group = parser.add_argument_group('General')
    # Help message
    group.add_argument('-h', '--help', action='help',
                       help='Show this help message and exit')
    # Print version number
    group.add_argument('-V', '--version', action='store_true',
                       help='Show version number and exit')
    return parser


def main():
    """Parse command line arguments and handle appropriately"""
    parser = get_parser()
    args = parser.parse_args()
    if args.version is not None and args.version:
        print('webdriver_test_tools ' + version.get_version_info()['version'])
        return
    if args.init:
        initialize.main()
    # If no arguments were specified, print help
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
