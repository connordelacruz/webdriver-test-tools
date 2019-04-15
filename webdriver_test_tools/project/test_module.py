"""Functions for test project ``__main__`` modules"""

from argparse import RawTextHelpFormatter

from webdriver_test_tools.common import cmd
from webdriver_test_tools.project.cmd.common import get_test_parent_parser
from webdriver_test_tools.project.cmd.run import add_run_subparser, parse_run_args
from webdriver_test_tools.project.cmd.list import add_list_subparser, parse_list_args
from webdriver_test_tools.project.cmd.new import add_new_subparser, parse_new_args


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


# Argument Parser

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
        formatter_class=RawTextHelpFormatter,
        add_help=False, prog=package_name, epilog=cmd.argparse.ARGPARSE_EPILOG
    )
    # Subparsers
    command_desc = 'Run \'{} <command> --help\' for details'.format(package_name)
    subparsers = parser.add_subparsers(
        title='Commands', description=command_desc, dest='command', metavar='<command>'
    )
    run_parser = add_run_subparser(subparsers, config_module, parents=[test_parent_parser])
    list_parser = add_list_subparser(subparsers, parents=[test_parent_parser])
    new_parser = add_new_subparser(subparsers, config_module)
    return parser
