import os
import re
import sys

from webdriver_test_tools.common import cmd
from webdriver_test_tools.project.initialize import initialize


def main(args):
    """Command line dialogs for initializing a test project

    This method takes the parsed command line arguments as a parameter. It's
    assumed that the ``init`` subparser was added to the ``ArgumentParser``
    object via the :func:`add_init_subparser()` method before parsing.

    The ``init`` subparser has optional arguments for each of this method's
    prompts. ``package_name`` is the only argument required to create the
    package, so this method will attempt to bypass input prompts if it's set to
    something other than ``None``.

    If ``package_name`` is ``None`` but one or more of the other parameters are
    not ``None``, this method will attempt to bypass their corresponding input
    prompts if the value passed as a parameter is valid.

    :param args: The ``Namespace`` object returned by ``parser.parse_args()``.
        It is assumed that the ``init`` subparser was added to the
        ``ArgumentParser`` that returned this ``Namespace``
    """
    # Retrieve values from args
    package_name=args.package_name
    project_title=args.project_title
    gitignore=args.no_gitignore
    readme=args.no_readme
    # For Ctrl + C handling
    initialize_start = False
    # Handle any optional arguments
    if package_name is not None:
        # project_title defaults to package_name if not specified
        if project_title is None:
            project_title = package_name
        # gitignore and readme default to True if not otherwise specified
        gitignore = 'y' if gitignore is None or gitignore else 'n'
        readme = 'y' if readme is None or readme else 'n'
    try:
        print(cmd.COLORS['title']('Test Project Initialization') + '\n')
        # Prompt for input if no package name is passed as a parameter
        validated_package_name = cmd.prompt(
            'Package name',
            'Enter a name for the test package',
            '(use only alphanumeric characters and underscores. Cannot start with a number)',
            validate=cmd.validate_package_name,
            parsed_input=package_name
        )
        # Prompt for optional project title, default to validated_package_name
        validated_project_title = cmd.prompt(
            'Project title',
            '(Optional) Enter a human-readable name for the test project',
            '(can use alphanumeric characters, spaces, hyphens, and underscores)',
            default=validated_package_name, validate=validate_project_title,
            parsed_input=project_title
        )
        # Ask if gitignore files should be generated
        gitignore_files = cmd.prompt(
            'Create .gitignore files (y/n)',
            'Create .gitignore files for project root and log directory?',
            '(Ignores python cache files, package install files, local driver logs, etc)',
            default='y', validate=cmd.validate_yn,
            parsed_input=gitignore
        )
        # Ask if README should be generated
        readme_file = cmd.prompt(
            'Create README file (y/n)',
            'Generate README file?',
            '(README contains information on command line usage and directory structure)',
            default='y', validate=cmd.validate_yn,
            parsed_input=readme
        )
        # Create project package
        print('Creating test project...')
        initialize_start = True
        initialize(os.getcwd(), validated_package_name, validated_project_title, gitignore_files, readme_file)
        print(cmd.COLORS['success']('Project initialized.') + '\n')
        print(
            'To get started, set the SITE_URL for the project in {}/config/site.py\n'.format(validated_package_name),
            'To create a new test, run:',
            cmd.INDENT + 'python -m {} new test <module_name> <TestCaseClass>\n'.format(validated_package_name),
            'To create a new page object, run:',
            cmd.INDENT + 'python -m {} new page <module_name> <PageObjectClass>\n'.format(validated_package_name),
            cmd.argparse.ARGPARSE_EPILOG, sep='\n'
        )
    except KeyboardInterrupt:
        print('')
        if initialize_start:
            msg = 'Initialization was cancelled mid-operation.'
            print(cmd.COLORS['warning'](msg))
        sys.exit()


# Subparser

def add_init_subparser(subparsers, parents=[]):
    """Add subparser for the ``wtt init`` command

    :param subparsers: ``argparse._SubParsersAction`` object for the ``wtt`` ArgumentParser (i.e. the object
        returned by the ``add_subparsers()`` method)
    :param parents: (Default: ``[]``) Parent parsers for the init subparser

    :return: ``argparse.ArgumentParser`` object for the newly added ``init`` subparser
    """
    init_description = 'Initialize a new test project in the current directory. \
        If no arguments are provided, a prompt will walk you through project initialization.'
    init_help = init_description
    init_parser = subparsers.add_parser(
        'init', description=init_description, help=init_help,
        epilog=cmd.argparse.ARGPARSE_EPILOG,
        parents=parents, add_help=False,
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
    optional_args_description = 'Override default behaviour when initializing a project from the command line.'
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
    return init_parser


# User Input Prompts

def validate_project_title(project_title):
    """Sanitizes string to avoid syntax errors when inserting the title into template
    files

    :param project_title: The desired project title

    :return: Modifed project_title with only alphanumeric characters, spaces,
        underscores, and hyphens
    """
    # Trim outer whitespace and remove that aren't alphanumeric or an underscore/hyphen
    validated_project_title = re.sub(r'[^\w\s-]', '', project_title.strip())
    if not validated_project_title:
        raise cmd.ValidationError('Please enter a valid project title.')
    # Alert user of any changes made in validation
    if project_title != validated_project_title:
        cmd.print_validation_change(
            '"{0}" was changed to "{1}" to avoid syntax errors',
            project_title, validated_project_title
        )
    return validated_project_title

