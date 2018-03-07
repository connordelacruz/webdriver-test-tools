# Used to create a new test package

import glob
import os
import shutil
import re
import jinja2

import webdriver_test_tools.templates


# Project creation functions
# ----------------------------------------------------------------

def create_test_directories(target_path):
    """Creates base directories for test writing (data, pages, and tests)

    :param target_path: The path to the test package directory
    """
    target_path = os.path.abspath(target_path)
    project_dirs = [
            'data',
            'pages',
            'tests',
            ]
    for project_dir in project_dirs:
        create_directory(target_path, project_dir)


def create_config_files(target_path):
    """Creates test package config directory and config files

    :param target_path: The path to the test package directory
    """
    target_path = create_directory(os.path.abspath(target_path), 'config')
    template_path = os.path.dirname(os.path.abspath(webdriver_test_tools.templates.config.__file__))
    # Get only .py files
    config_files = [os.path.basename(file) for file in glob.glob(os.path.join(template_path, '*.py'))]
    for config_file in config_files:
        source_file = os.path.join(template_path, config_file)
        # Precautionary check that this is a file
        if os.path.isfile(source_file):
            target_file = os.path.join(target_path, config_file)
            shutil.copy(source_file, target_file)


def create_template_files(target_path, context):
    """Creates test package template directory and template files

    :param target_path: The path to the test package directory
    :param context: Jinja context used to render template
    """
    target_path = create_directory(os.path.abspath(target_path), 'templates')
    template_path = os.path.dirname(os.path.abspath(webdriver_test_tools.templates.__file__))
    # Copy over page_object.py since it doesn't really need any changes
    page_object_file = 'page_object.py'
    page_object_source = os.path.join(template_path, page_object_file)
    page_object_target = os.path.join(target_path, page_object_file)
    shutil.copy(page_object_source, page_object_target)
    # Render a template for test_case.py and copy that over
    test_case_file = 'test_case.py'
    test_case_template = os.path.join(template_path, test_case_file)
    test_case_target = os.path.join(target_path, test_case_file)
    render_template_to_file(test_case_template, context, test_case_target)


def create_package_directory(target_path, package_name):
    """Creates package directory for test project

    :param target_path: The path to the outer directory where initialize was called
    :param package_name: The desired name of the package (will be validated)

    :return: Path to created package directory
    """
    target_path = os.path.abspath(target_path)
    package_directory = validate_package_name(package_name)
    return create_directory(target_path, package_directory)


# TODO: create __init__.py and __main__.py as necessary

def create_setup_file(target_path, context):
    """Creates setup.py for test project

    :param target_path: The path to the outer directory where the package directory is contained
    :param context: Jinja context used to render template
    """
    target_path = os.path.abspath(target_path)
    template_path = os.path.dirname(os.path.abspath(webdriver_test_tools.templates.__file__))
    setup_file = 'setup.py'
    setup_template = os.path.join(template_path, setup_file)
    setup_target = os.path.join(target_path, setup_file)
    render_template_to_file(setup_template, context, setup_target)


def create_readme(target_path, context):
    """Create README.md for test project

    :param target_path: The path to the outer directory where the package directory is contained
    :param context: Jinja context used to render template
    """
    target_path = os.path.abspath(target_path)
    template_path = os.path.dirname(os.path.abspath(webdriver_test_tools.templates.__file__))
    readme_file = 'README.md'
    readme_template = os.path.join(template_path, readme_file)
    readme_target = os.path.join(target_path, readme_file)
    render_template_to_file(readme_template, context, readme_target)



# Helper functions
# ----------------------------------------------------------------

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


def validate_package_name(package_name):
    """Removes and replaces characters to ensure a string is a valid python package
    name

    :param package_name: The desired package name

    :return: Modified package_name with whitespaces and hyphens replaced with
    underscores and all invalid characters removed
    """
    # Trim outer whitespace and replace inner whitespace and hyphens with underscore
    package_name = re.sub(r'\s+|-+', '_', package_name.strip())
    # Remove non-alphanumeric or _ characters
    package_name = re.sub(r'[^\w\s]', '', package_name)
    # Remove leading characters until we hit a letter or underscore
    # TODO: remove leading underscore too?
    package_name = re.sub(r'^[^a-zA-Z_]+', '', package_name)
    return package_name


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


# TODO: update as more templates are created
def generate_context(test_package):
    """Returns a jinja context to use for rendering templates

    :param test_package: Name of the python test package
    """
    context = {
            'test_package': test_package
            }
    return context


# Main methods
# ----------------------------------------------------------------

def initialize(target_path, package_name):
    """Initializes new project package

    :param target_path: Path to directory that will contain test package
    :param package_name: Name of the test package to create (will be validated)
    """
    outer_path = os.path.abspath(target_path)
    package_name = validate_package_name(package_name)
    context = generate_context(package_name)
    # Initialize files in the outer directory
    create_setup_file(outer_path, context)
    create_readme(outer_path, context)
    package_path = create_package_directory(outer_path, package_name)
    # Initialize package files
    create_test_directories(package_path)
    create_config_files(package_path)
    create_template_files(package_path, context)


# TODO: optional param for package_name that skips input dialog if not None (can be used to add an example test project in the future)
def main():
    # TODO: document
    print('Enter a name for the test package')
    print('(use only alphanumeric characters and underscores. Cannot start with a number)')
    # TODO: add more robust input validation
    package_name = input('Package name: ')
    validated_package_name = validate_package_name(package_name)
    # Alert user of any changes made in validation
    if package_name != validated_package_name:
        message_format = 'Name was changed to {} in order to be a valid python package'
        print(message_format.format(validated_package_name))
    # Create project package
    print('Creating test project...')
    initialize(os.getcwd(), validated_package_name)
    # TODO: catch errors? More robust output?
    print('Project initialized.')


if __name__ == '__main__':
    main()




