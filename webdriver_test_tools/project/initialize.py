# Used to create a new test package

import glob
import os
import shutil
import re
import jinja2
from blessings import Terminal

import webdriver_test_tools.project.templates
from webdriver_test_tools.version import __version__, __selenium__


# For formatted terminal output
term = Terminal()

# Prepend to input prompts
PROMPT_PREFIX = '> '

# Project creation functions

def create_test_directories(target_path):
    """Creates base directories for test writing that are initially empty (data/ and pages/)

    :param target_path: The path to the test package directory
    """
    target_path = os.path.abspath(target_path)
    project_dirs = [
            'data',
            'pages',
            ]
    for project_dir in project_dirs:
        create_directory(target_path, project_dir)


def create_log_directory(target_path):
    """Creates log/ directory and log/.gitignore file

    :param target_path: The path to the test package directory
    """
    target_path = os.path.abspath(target_path)
    source_path = os.path.dirname(os.path.abspath(webdriver_test_tools.project.templates.log.__file__))
    log_path = create_directory(target_path, 'log')
    filename = '.gitignore'
    shutil.copy(os.path.join(source_path, filename), os.path.join(log_path, filename))


def create_tests_init(target_path, context):
    """Creates test package tests/ subdirectory and tests/__init__.py

    :param target_path: The path to the test package directory
    :param context: Jinja context used to render template
    """
    target_path = create_directory(os.path.abspath(target_path), 'tests')
    template_path = os.path.dirname(os.path.abspath(webdriver_test_tools.project.templates.tests.__file__))
    create_file_from_template(template_path, target_path, '__init__.py', context)


def create_config_files(target_path, context):
    """Creates test package config directory and config files

    :param target_path: The path to the test package directory
    :param context: Jinja context used to render template
    """
    target_path = create_directory(os.path.abspath(target_path), 'config')
    template_path = os.path.dirname(os.path.abspath(webdriver_test_tools.project.templates.config.__file__))
    # Non-template config files
    config_files = [
        'browser.py',
        'site.py',
        'test.py',
    ]
    for config_file in config_files:
        source_file = os.path.join(template_path, config_file)
        # Precautionary check that this is a file
        if os.path.isfile(source_file):
            target_file = os.path.join(target_path, config_file)
            shutil.copy(source_file, target_file)
    # .j2 template files
    template_files = [
        '__init__.py',
        'browserstack.py',
        'webdriver.py',
    ]
    for template_file in template_files:
        create_file_from_template(template_path, target_path, template_file, context)


def create_template_files(target_path, context):
    """Creates test package template directory and template files

    :param target_path: The path to the test package directory
    :param context: Jinja context used to render template
    """
    target_path = create_directory(os.path.abspath(target_path), 'templates')
    template_path = os.path.dirname(os.path.abspath(webdriver_test_tools.project.templates.templates.__file__))
    # Copy over page_object.py since it doesn't really need any changes
    page_object_file = 'page_object.py'
    page_object_source = os.path.join(template_path, page_object_file)
    page_object_target = os.path.join(target_path, page_object_file)
    shutil.copy(page_object_source, page_object_target)
    # Render a template for test_case.py and copy that over
    create_file_from_template(template_path, target_path, 'test_case.py', context)


def create_package_directory(target_path, package_name):
    """Creates package directory for test project

    :param target_path: The path to the outer directory where initialize was called
    :param package_name: The desired name of the package (will be validated)

    :return: Path to created package directory
    """
    target_path = os.path.abspath(target_path)
    package_directory = validate_package_name(package_name)
    return create_directory(target_path, package_directory)


def create_main_module(target_path, context):
    """Creates __main__.py and __init__.py modules for test package

    :param target_path: The path to the test package directory
    :param context: Jinja context used to render template
    """
    target_path = os.path.abspath(target_path)
    template_path = os.path.dirname(os.path.abspath(webdriver_test_tools.project.templates.__file__))
    create_file_from_template(template_path, target_path, '__main__.py', context)
    # "Touch" __init__.py to create an empty file
    init_path = os.path.join(target_path, '__init__.py')
    open(init_path, 'a').close()


def create_setup_file(target_path, context):
    """Creates setup.py for test project

    :param target_path: The path to the outer directory where the package directory is contained
    :param context: Jinja context used to render template
    """
    target_path = os.path.abspath(target_path)
    template_path = os.path.dirname(os.path.abspath(webdriver_test_tools.project.templates.__file__))
    create_file_from_template(template_path, target_path, 'setup.py', context)


def create_readme(target_path, context):
    """Create README.rst for test project

    :param target_path: The path to the outer directory where the package directory is contained
    :param context: Jinja context used to render template
    """
    target_path = os.path.abspath(target_path)
    template_path = os.path.dirname(os.path.abspath(webdriver_test_tools.project.templates.__file__))
    create_file_from_template(template_path, target_path, 'README.rst', context)


def create_gitignore(target_path):
    """Create .gitignore file at the root of the test project

    :param target_path: The path to the outer directory where the package directory is contained
    """
    target_path = os.path.abspath(target_path)
    source_path = os.path.dirname(os.path.abspath(webdriver_test_tools.project.templates.__file__))
    filename = '.gitignore'
    shutil.copy(os.path.join(source_path, filename), os.path.join(target_path, filename))


# Helper functions

def create_directory(target_path, directory_name):
    """Creates a directory in the target path if it doesn't already exist

    :param target_path: The path to the directory that will contain the new one
    :param directory_name: The name of the directory to create in the target path

    :return: The path to the newly created (or already existing) directory
    """
    path = os.path.join(target_path, directory_name)
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def render_template_to_file(template_path, context, target_path):
    """Writes rendered jinja template to a file

    :param template_path: The path to the jinja template
    :param context: Jinja context used to render template
    :param target_path: File path to write the rendered template to
    """
    with open(target_path, 'w') as f:
        file_contents = render_template(template_path, context)
        f.write(file_contents)


def render_template(template_path, context):
    """Returns the rendered contents of a jinja template

    :param template_path: The path to the jinja template
    :param context: Jinja context used to render template

    :return: Results of rendering jinja template
    """
    path, filename = os.path.split(template_path)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(context)


def generate_context(test_package, test_tools_version, selenium_version, project_title=None):
    """Returns a jinja context to use for rendering templates

    :param test_package: Name of the python test package
    :param test_tools_version: Version of webdriver_test_tools to use as install
        dependency
    :param selenium_version: Version of selenium package used when developing/testing
        the current version of webdriver_test_tools
    :param project_title: (Default = test_package) Human-readable title for the test
        project. Defaults to the value of test_package if not provided

    :return: Dictionary to use as a context when rendering Jinja templates
    """
    if project_title is None:
        project_title = test_package

    context = {
            'test_package': test_package,
            'test_tools_version': test_tools_version,
            'selenium_version': selenium_version,
            'project_title': project_title,
            }
    return context


def create_file_from_template(template_path, target_path, filename, context):
    """Short hand function that renders a template with the specified filename followed by a '.j2' extension from the template path to a file with the specified name in the target path

    The use of '.j2' as a file extension is to distinguish templates from package modules.

    :param template_path: Path to template directory
    :param target_path: Path to target directory
    :param filename: Name of the template file. Will be used as the filename for the rendered file written to the target directory
    :param context: Jinja context used to render template
    """
    file_template = os.path.join(template_path, filename + '.j2')
    file_target = os.path.join(target_path, filename)
    render_template_to_file(file_template, context, file_target)


# Prompt helper methods

class ValidationError(Exception):
    """Exception raised if input validation fails"""
    pass


def nonempty(text):
    """Input validation function. Raises ValidationError if text is empty

    :param text: Text to validate

    :return: Validated text
    """
    if not text:
        raise ValidationError('Please enter some text.')
    return text


def validate_package_name(package_name):
    """Removes and replaces characters to ensure a string is a valid python package name

    :param package_name: The desired package name

    :return: Modified package_name with whitespaces and hyphens replaced with underscores and all invalid characters removed
    """
    # Trim outer whitespace and replace inner whitespace and hyphens with underscore
    validated_package_name = re.sub(r'\s+|-+', '_', package_name.strip())
    # Remove non-alphanumeric or _ characters
    validated_package_name = re.sub(r'[^\w\s]', '', validated_package_name)
    # Remove leading characters until we hit a letter or underscore
    validated_package_name = re.sub(r'^[^a-zA-Z_]+', '', validated_package_name)
    if not validated_package_name:
        raise ValidationError('Please enter a valid package name.')
    # Alert user of any changes made in validation
    if package_name != validated_package_name:
        message_format = 'Name was changed to {} in order to be a valid python package'
        print(term.yellow(message_format.format(validated_package_name)))
    return validated_package_name


def validate_project_title(project_title):
    """Sanitizes string to avoid syntax erros when inserting the title into template
    files

    :param project_title: The desired project title

    :return: Modifed project_title with only alphanumeric characters, spaces, underscores, and hyphens
    """
    # Trim outer whitespace and remove that aren't alphanumeric or an underscore/hyphen
    validated_project_title = re.sub(r'[^\w\s-]', '', project_title.strip())
    if not validated_project_title:
        raise ValidationError('Please enter a valid project title.')
    # Alert user of any changes made in validation
    if project_title != validated_project_title:
        message_format = 'Title was changed to {} to avoid syntax errors.'
        print(term.yellow(message_format.format(validated_project_title)))
    return validated_project_title


def prompt(text, default=None, validate=nonempty, trailing_newline=True):
    """Prompt the user for input and validate it

    :param text: Text to display in prompt
    :param default: (Optional) default value
    :param validate: (Default = nonempty) Validation function for input
    :param trailing_newline: (Default = True) Print a blank line after receiving user input and successfully validating

    :return: Validated input
    """
    prompt_text = '{} [{}]: '.format(text, default) if default is not None else text + ': '
    prompt_text = term.magenta(PROMPT_PREFIX + prompt_text)
    while True:
        val = input(prompt_text).strip()
        if default is not None and not val:
            val = default
        try:
            val = validate(val)
        except ValidationError as e:
            print(term.bold_red(str(e)))
            continue
        break
    if trailing_newline:
        print('')
    return val


# Main methods

def initialize(target_path, package_name, project_title):
    """Initializes new project package

    :param target_path: Path to directory that will contain test package
    :param package_name: Name of the test package to create (will be validated)
    :param project_title: Human readable title of the test project.
    """
    outer_path = os.path.abspath(target_path)
    package_name = validate_package_name(package_name)
    context = generate_context(package_name, __version__, __selenium__, project_title)
    # Initialize files in the outer directory
    create_setup_file(outer_path, context)
    create_readme(outer_path, context)
    create_gitignore(outer_path)
    package_path = create_package_directory(outer_path, package_name)
    # Initialize package files
    create_main_module(package_path, context)
    create_test_directories(package_path)
    create_log_directory(package_path)
    create_tests_init(package_path, context)
    create_config_files(package_path, context)
    create_template_files(package_path, context)


# TODO: implement optional params
def main(package_name=None, project_title=None):
    """Command line dialogs for initializing a test project

    :param package_name: (Optional) If specified, the prompt asking the user to enter a
        package name will be skipped and function will continue using this as the
        package name
    :param project_title: (Optional) If specified, the prompt asking the user to enter a
        project title will be skipped and function will continue using this as the
        project title
    """
    print(term.bold('webdriver_test_tools {} project initialization'.format(__version__)) + '\n')
    # Prompt for input if no package name is passed as a parameter
    print('Enter a name for the test package')
    print('(use only alphanumeric characters and underscores. Cannot start with a number)')
    validated_package_name = prompt('Package name', validate=validate_package_name)
    # Prompt for optional project title, default to validated_package_name
    print('(Optional) Enter a human-readable name for the test project')
    print('(can use alphanumeric characters, spaces, hyphens, and underscores)')
    validated_project_title = prompt('Project title', default=validated_package_name, validate=validate_project_title)
    # Create project package
    print('Creating test project...')
    initialize(os.getcwd(), validated_package_name, validated_project_title)
    print(term.green('Project initialized.') + '\n')
    print(term.bold('To get started, set the SITE_URL for the project in {}/config/site.py'.format(validated_package_name)))


if __name__ == '__main__':
    main()


