import os
import sys
from argparse import RawTextHelpFormatter, SUPPRESS

from webdriver_test_tools import config
from webdriver_test_tools.common import cmd
from webdriver_test_tools.project import new_file


def main(test_package_path, test_package, args):
    """Command line dialogs for creating a new file

    This method checks ``args`` for optional arguments for each of its prompts.
    If these are set to something other than ``None``, their corresponding
    input prompts will be skipped unless validation for that parameter fails.

    ``type``, ``module_name``, and ``class_name`` are the 3 values required to
    create a new file. If these are all set to something other than ``None``,
    this method will default to an empty ``description`` unless one is
    provided.

    ``force`` is the only optional parameter that does not have a prompt. It
    will default to ``False`` unless the ``--force`` flag is used when calling
    this method.

    The ``new page`` command has additional optional arguments ``--prototype``
    and ``--yaml``/``--no-yaml`` (depending on the configuration of
    ``ProjectFilesConfig.ENABLE_PAGE_OBJECT_YAML``). Prompt for ``--prototype``
    will not be shown if ``type``, ``module_name``, and ``class_name`` are all
    set to something other than ``None``. Instead, this method will use the
    standard page object template unless one is specified with ``prototype``.
    Currently there is no prompt for the ``--yaml``/``--no-yaml`` arguments, so
    the value of ``ProjectFilesConfig.ENABLE_PAGE_OBJECT_YAML`` will always be
    used unless ``--yaml``/``--no-yaml`` is specified.

    :param test_package_path: The root directory of the test package
    :param test_package: The python package name of the test package
    :param args: Parsed arguments for the ``new`` command
    """
    new_file_start = False
    # Get common items from args
    # (Using getattr() with default values because some attributes might not be
    # present if args.type wasn't specified)
    file_type = getattr(args, 'type', None)
    module_name = getattr(args, 'module_name', None)
    class_name = getattr(args, 'class_name', None)
    description = getattr(args, 'description', None)
    force = getattr(args, 'force', False)
    # module and class names are the minimum required args, will ignore
    # optional prompts if this is True
    minimum_required_args = module_name and class_name
    try:
        # if module_name and class_name are set, use defaults for optional arguments
        if minimum_required_args and description is None:
            description = ''
        _validate_file_type = cmd.validate_choice(
            [new_file.TEST_TYPE, new_file.PAGE_TYPE],
            shorthand_choices={'t': new_file.TEST_TYPE, 'p': new_file.PAGE_TYPE}
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
            validate=cmd.validate_module_name,
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
        # Arguments for page-specific prompts
        kwargs = {}
        if validated_file_type == new_file.PAGE_TYPE:
            prototype = getattr(args, 'prototype', None)
            use_yaml = getattr(args, 'use_yaml', config.ProjectFilesConfig.ENABLE_PAGE_OBJECT_YAML)
            if prototype is None and minimum_required_args:
                prototype = ''
            _prototype_choices = [name for name in new_file.PROTOTYPE_NAMES]
            # Allow for numeric shorthand answers (starting at 1)
            _prototype_shorthands = {
                str(ind + 1): choice for ind, choice in enumerate(_prototype_choices)
            }
            # Allow empty string since this is an optional parameter
            _prototype_choices.append('')
            _validate_prototype = cmd.validate_choice(
                _prototype_choices, shorthand_choices=_prototype_shorthands
            )
            kwargs['prototype'] = cmd.prompt(
                'Page object prototype',
                '(Optional) Select a page object prototype to subclass:',
                *[cmd.INDENT + '[{}] {}'.format(i, name) for i, name in _prototype_shorthands.items()],
                validate=_validate_prototype,
                default='',
                parsed_input=prototype
            )
            # TODO: Add prompt if class supports it (will need to change arg default to None and pass config_module as param)
            kwargs['use_yaml'] = use_yaml
        # Start file creation
        new_file_start = True
        new_file_paths = new_file.new_file(
            test_package_path, test_package,
            file_type=validated_file_type, module_name=validated_module_name,
            class_name=validated_class_name, description=validated_description,
            force=force, **kwargs
        )
        # Output new file path on success
        # TODO: Custom success messages based on type? E.g. instructions on filling out YAML file?
        success_msg = '\nFile' + ('s' if len(new_file_paths) > 1 else '') + ' created.'
        print(cmd.COLORS['success'](success_msg))
        for new_file_path in new_file_paths:
            print(new_file_path)
    except KeyboardInterrupt:
        print('')
        if new_file_start:
            msg = 'File creation was cancelled mid-operation.'
            print(cmd.COLORS['warning'](msg))
        sys.exit()


# Subparser

def add_new_subparser(subparsers, config_module, formatter_class=RawTextHelpFormatter):
    """Add subparser for the ``<test_package> new`` command

    :param subparsers: ``argparse._SubParsersAction`` object for the test
        package ArgumentParser (i.e. the object returned by the
        ``add_subparsers()`` method)
    :param config_module: The module object for ``<test_project>.config``
    :param formatter_class: (Default: ``argparse.RawTextHelpFormatter``) Class
        to use for the ``formatter_class`` parameter

    :return: ``argparse.ArgumentParser`` object for the newly added ``new``
        subparser
    """
    if config_module is None:
        config_module = config
    # Get ProjectFilesConfig
    project_files_config = config_module.ProjectFilesConfig if 'ProjectFilesConfig' in dir(config_module) else config.ProjectFilesConfig
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
    _add_new_test_subparser(formatter_class, generic_parent_parser, new_subparsers, project_files_config)
    # New page object parser
    _add_new_page_subparser(formatter_class, generic_parent_parser, new_subparsers, project_files_config)
    return new_parser


def _add_new_test_subparser(formatter_class, generic_parent_parser, new_subparsers, project_files_config):
    """Add subparser for ``new test`` command

    :param formatter_class: Class to use for the ``formatter_class`` parameter
    :param generic_parent_parser: Generic parent parser to use for the
        ``parents`` parameter
    :param new_subparsers: The subparser for the ``new`` command
    :param project_files_config: The ``ProjectFilesConfig`` class
    """
    new_test_parent_parser = get_new_parent_parser(
        parents=[generic_parent_parser], class_name_metavar='<TestCaseClass>',
        class_name_help='Name to use for the initial test case class'
    )
    new_test_description = 'Create a new test module'
    new_test_help = new_test_description
    new_subparsers.add_parser(
        'test', description=new_test_description, help=new_test_help,
        parents=[new_test_parent_parser],
        formatter_class=formatter_class,
        add_help=False, epilog=cmd.argparse.ARGPARSE_EPILOG
    )


def _add_new_page_subparser(formatter_class, generic_parent_parser, new_subparsers, project_files_config):
    """Add subparser for ``new page`` command

    :param formatter_class: Class to use for the ``formatter_class`` parameter
    :param generic_parent_parser: Generic parent parser to use for the
        ``parents`` parameter
    :param new_subparsers: The subparser for the ``new`` command
    :param project_files_config: The ``ProjectFilesConfig`` class
    """
    new_page_parent_parser = get_new_parent_parser(
        parents=[generic_parent_parser], class_name_metavar='<PageObjectClass>',
        class_name_help='Name to use for the initial page object class'
    )
    new_page_description = 'Create a new page object module'
    new_page_help = new_page_description
    new_page_parser = new_subparsers.add_parser(
        'page', description=new_page_description, help=new_page_help,
        parents=[new_page_parent_parser],
        formatter_class=formatter_class,
        add_help=False, epilog=cmd.argparse.ARGPARSE_EPILOG
    )
    prototype_group = new_page_parser.add_argument_group('Prototype Options')
    prototype_options_help = _format_prototype_choices()
    prototype_help = 'Page object prototype to subclass.' + prototype_options_help
    prototype_group.add_argument('-p', '--prototype', metavar='<prototype_choice>', default=None,
                                 choices=new_file.PROTOTYPE_NAMES, help=prototype_help)
    yaml_default = project_files_config.ENABLE_PAGE_OBJECT_YAML
    # Add options to negate YAML default config
    if yaml_default:
        no_yaml_help = 'Only generate .py files if using a --prototype that supports YAML parsing' + _format_yaml_prototype_choices()
        yaml_help = SUPPRESS
    else:
        yaml_help = 'Generate .py and .yml files if using a --prototype that supports YAML parsing' + _format_yaml_prototype_choices()
        no_yaml_help = SUPPRESS
    yaml_group = prototype_group.add_mutually_exclusive_group()
    yaml_group.add_argument('--yaml', '-y', action='store_true', default=yaml_default,
                                 dest='use_yaml', help=yaml_help)
    yaml_group.add_argument('--no-yaml', '-Y', action='store_false', default=yaml_default,
                                 dest='use_yaml', help=no_yaml_help)


def _format_prototype_choices():
    """Format the help string for page object prototype choices

    The returned string will have the following format:

    .. code:: python

        '\\nOptions: {prototype,"prototype with spaces"}'

    :return: Formatted help string for prototype options
    """
    # Add quotes around names with spaces
    formatted_prototype_names = [
        '"{}"'.format(name) if ' ' in name else name
        for name in new_file.PROTOTYPE_NAMES
    ]
    return '\nOptions: {{{}}}'.format(','.join(formatted_prototype_names))


def _format_yaml_prototype_choices():
    """Format the help string for prototype choices with YAML support

    The returned string will have the following format:

    .. code:: python

        '\\nSupported Prototypes: {prototype,"prototype with spaces"}'

    :return: Formatted help string for prototype options
    """
    # Add quotes around names with spaces
    formatted_prototype_names = [
        '"{}"'.format(name) if ' ' in name else name
        for name in new_file.YAML_PROTOTYPE_NAMES
    ]
    return '\nSupported Prototypes: {{{}}}'.format(','.join(formatted_prototype_names))


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
    positional_args_group = new_parent_parser.add_argument_group('Positional Arguments')
    # Positional arguments
    module_name_help = 'Filename to use for the new python module'
    positional_args_group.add_argument('module_name', metavar='<module_name>', nargs='?', default=None,
                                   help=module_name_help)
    positional_args_group.add_argument('class_name', metavar=class_name_metavar, nargs='?', default=None,
                                   help=class_name_help)
    # Optional arguments
    optional_args_group = new_parent_parser.add_argument_group('Optional Arguments')
    description_help='Description for the initial class'
    optional_args_group.add_argument('-d', '--description', metavar='<description>', default=None,
                                   help=description_help)
    force_help='Force overwrite if a file with the same name already exists'
    optional_args_group.add_argument('-f', '--force', action='store_true', default=False,
                                   help=force_help)

    return new_parent_parser


# Argument parsing functions

# TODO: DOC exceptions that may be raised
def parse_new_args(package_name, tests_module, args):
    """Parse arguments and run the 'new' command

    :param package_name: Name of the test package
    :param tests_module: The module object for ``<test_project>.tests``. Used
        to determine the filepath of the package
    :param args: The namespace returned by parser.parse_args()

    :return: Exit code, 0 if files were created without exceptions, 1 otherwise.

        .. note::

            Technically, this will always return 0, as all fail states cause an
            exception to be raised. This is just to keep it consistent with
            other project cmd parse arg functions.
    """
    exit_code = 0
    # Get package path based on tests_module path
    test_package_path = os.path.dirname(os.path.dirname(tests_module.__file__))
    main(test_package_path, package_name, args)
    return exit_code


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

