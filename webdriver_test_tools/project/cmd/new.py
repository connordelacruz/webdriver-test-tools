import argparse
import os

from webdriver_test_tools import cmd
from webdriver_test_tools.project import new_file


def add_new_subparser(subparsers):
    """Add subparser for the ``<test_package> new`` command

    :param subparsers: ``argparse._SubParsersAction`` object for the test package ArgumentParser (i.e. the object
        returned by the ``add_subparsers()`` method)

    :return: ``argparse.ArgumentParser`` object for the newly added ``new`` subparser
    """
    # TODO: add info on no args to description or help
    # Adds custom --help argument
    generic_parent_parser = cmd.argparse.get_generic_parent_parser()
    new_description = 'Create a new test module or page object'
    new_help = new_description
    new_parser = subparsers.add_parser(
        'new', description=new_description, help=new_help,
        parents=[generic_parent_parser],
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False, epilog=cmd.argparse.ARGPARSE_EPILOG
    )
    # New <type> subparsers
    new_type_desc = 'Run \'{} <type> --help\' for details'.format(new_parser.prog)
    new_subparsers = new_parser.add_subparsers(
        title='File Types', description=new_type_desc, dest='type', metavar='<type>'
    )
    # New test parser
    new_test_parent_parser = get_new_parent_parser(
        parents=[generic_parent_parser], class_name_metavar='<TestCaseClass>',
        class_name_help='Name to use for the initial test case class'
    )
    new_test_description = 'Create a new test module'
    new_test_help = new_test_description
    new_subparsers.add_parser(
        'test', description=new_test_description, help=new_test_help,
        parents=[new_test_parent_parser],
        add_help=False, epilog=cmd.argparse.ARGPARSE_EPILOG
    )
    # New page object parser
    new_page_parent_parser = get_new_parent_parser(
        parents=[generic_parent_parser], class_name_metavar='<PageObjectClass>',
        class_name_help='Name to use for the initial page object class'
    )
    new_page_description = 'Create a new page object module'
    new_page_help = new_page_description
    new_page_parser = new_subparsers.add_parser(
        'page', description=new_page_description, help=new_page_help,
        parents=[new_page_parent_parser],
        add_help=False, epilog=cmd.argparse.ARGPARSE_EPILOG
    )
    # TODO: add optional --prototype arg with a list of valid page object prototype classes
    return new_parser


def get_new_parent_parser(parents=[], class_name_metavar='<ClassName>',
                          class_name_help='Name to use for the initial class'):
    """Returns an :class:`ArgumentParser
    <webdriver_test_tools.cmd.argparse.ArgumentParser>` with ``<module_name>``,
    ``<class_name>``, and ``--description`` arguments

    :param parents: (Optional) List of ``ArgumentParser`` objects to use as
        parents for the test argument parser
    :param class_name_metavar: (Optional) Metavar to display for the class_name
        argument
    :param class_name_help: (Optional) Help text to use for the class_name
        argument

    :return: :class:`ArgumentParser
        <webdriver_test_tools.cmd.argparse.ArgumentParser>` with
        ``<module_name>``, ``<class_name>``, and ``--description`` arguments
    """
    new_parent_parser = cmd.argparse.ArgumentParser(add_help=False, parents=parents)
    # Positional arguments
    module_name_help = 'Filename to use for the new python module'
    new_parent_parser.add_argument('module_name', metavar='<module_name>', nargs='?', default=None,
                                   help=module_name_help)
    new_parent_parser.add_argument('class_name', metavar=class_name_metavar, nargs='?', default=None,
                                   help=class_name_help)
    # Optional arguments
    description_help='Description for the initial class'
    new_parent_parser.add_argument('-d', '--description', metavar='<description>', default=None,
                                   help=description_help)
    force_help='Force overwrite if a file with the same name already exists'
    new_parent_parser.add_argument('-f', '--force', action='store_true', default=False,
                                   help=force_help)

    return new_parent_parser


def parse_new_args(package_name, tests_module, args):
    """Parse arguments and run the 'new' command

    :param package_name: Name of the test package
    :param tests_module: The module object for ``<test_project>.tests``. Used
        to determine the filepath of the package
    :param args: The namespace returned by parser.parse_args()
    """
    # Get package path based on tests_module path
    test_package_path = os.path.dirname(os.path.dirname(tests_module.__file__))
    try:
        # Account for event where user doesn't provide positional args for 'new' command
        if args.type is None:
            new_file.main(test_package_path, package_name)
        else:
            new_file.main(
                test_package_path, package_name, args.type, args.module_name,
                args.class_name, description=args.description, force=args.force
            )
    except Exception as e:
        print('')
        cmd.print_exception(e)
