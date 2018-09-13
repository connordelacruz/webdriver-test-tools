import os
import sys
from argparse import RawTextHelpFormatter

from webdriver_test_tools.common import cmd
from webdriver_test_tools.project import new_file


def main(test_package_path, test_package,
         file_type=None, module_name=None, class_name=None,
         description=None, force=False):
    """Command line dialogs for creating a new file

    This method accepts optional arguments for each of its prompts. If these
    are set to something other than ``None``, their corresponding input prompts
    will be skipped unless validation for that parameter fails.

    ``file_type``, ``module_name``, and ``class_name`` are the 3 values
    required to create a new file. If these are all set to something other than
    ``None``, this method will default to an empty ``description`` unless one
    is provided.

    ``force`` is the only optional parameter that does not have a prompt. It
    will default to ``False`` unless the ``--force`` flag is used when calling
    this method.

    :param test_package_path: The root directory of the test package
    :param test_package: The python package name of the test package
    :param file_type: (Optional) The type of file to create. If valid, the user
        won't be prompted for input and this will be used instead. Valid file
        types are stored as global variables with the _TYPE suffix
    :param module_name: (Optional) Filename to use for the new python module.
        If valid, the user won't be prompted for input and this will be used
        instead
    :param class_name: (Optional) Name to use for the initial test class.
        If valid, the user won't be prompted for input and this will be used
        instead
    :param description: (Optional) Description to use in the docstring of the
        initial class. User will only be prompted for a description if one or
        more of the positional arguments (``file_type``, ``module_name``, and
        ``class_name``) are set to ``None``
    :param force: (Default: False) If True, force overwrite if a file with the
        same name already exists
    """
    new_file_start = False
    try:
        # if module_name and class_name are set, use defaults for description and force
        if module_name and class_name and description is None:
            description = ''
        _validate_file_type = cmd.validate_choice(
            ['test','page'], shorthand_choices={'t': 'test', 'p': 'page'}
        )
        validated_file_type = cmd.prompt(
            '[t]est/[p]age',
            'Create a new test case or page object?',
            validate=_validate_file_type,
            parsed_input=file_type
        )
        validated_module_name = cmd.prompt(
            'Module file name',
            'Enter a file name for the new {} module'.format(validated_file_type),
            validate=cmd.validate_module_filename,
            parsed_input=module_name
        )
        class_type = 'test case' if validated_file_type == 'test' else 'page object'
        validated_class_name = cmd.prompt(
            '{} class name'.format(class_type.capitalize()),
            'Enter a name for the initial {} class'.format(class_type),
            validate=cmd.validate_class_name,
            parsed_input=class_name
        )
        validated_description = cmd.prompt(
            'Description',
            '(Optional) Enter description of the new {} class'.format(class_type),
            validate=validate_description,
            default='',
            parsed_input=description
        )
        new_file_start = True
        new_file_path = new_file.new_file(
            test_package_path, test_package,
            file_type=validated_file_type, module_name=validated_module_name,
            class_name=validated_class_name, description=validated_description,
            force=force
        )
        # Output new file path on success
        print(cmd.COLORS['success']('\nFile created.'))
        print(new_file_path)
    except KeyboardInterrupt:
        print('')
        if new_file_start:
            msg = 'File creation was cancelled mid-operation.'
            print(cmd.COLORS['warning'](msg))
        sys.exit()


# Subparser

def add_new_subparser(subparsers, formatter_class=RawTextHelpFormatter):
    """Add subparser for the ``<test_package> new`` command

    :param subparsers: ``argparse._SubParsersAction`` object for the test package ArgumentParser (i.e. the object
        returned by the ``add_subparsers()`` method)
    :param formatter_class: (Default: ``argparse.RawTextHelpFormatter``) Class to use for the ``formatter_class``
        parameter

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
        formatter_class=formatter_class,
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


# Argument parsing functions

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
            main(test_package_path, package_name)
        else:
            main(
                test_package_path, package_name, args.type, args.module_name,
                args.class_name, description=args.description, force=args.force
            )
    except Exception as e:
        print('')
        cmd.print_exception(e)


# User Input Prompts

def validate_description(description):
    """Replaces double quotes with single quotes in class description

    If the description is ``None`` or an empty string, this function considers
    it valid and returns ``None``

    :param description: The desired description string

    :return: Validated description string with double quotes replaced with
        single quotes or ``None`` if the description is empty
    """
    if description is None or description == '':
        return None
    # Replace double quotes with single quotes to avoid breaking the docstring
    validated_description = description.replace('"', "'")
    if validated_description != description:
        cmd.print_info('Replaced double quotes with single quotes in class description')
    return validated_description
