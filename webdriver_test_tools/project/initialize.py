"""Functions for creating a new test package."""

import shutil

from webdriver_test_tools.common.files import *
from webdriver_test_tools.__about__ import __version__, __selenium__
from webdriver_test_tools.project import templates


# Project creation functions

# Project Root

def create_setup_file(target_path, context):
    """Creates setup.py for test project

    :param target_path: The path to the outer directory where the package directory is
        contained
    :param context: Jinja context used to render template
    """
    target_path = os.path.abspath(target_path)
    template_path = templates.project_root.get_path()
    create_file_from_template(template_path, target_path, 'setup.py', context)


def create_readme(target_path, context):
    """Create README.rst for test project

    :param target_path: The path to the outer directory where the package directory is
        contained
    :param context: Jinja context used to render template
    """
    target_path = os.path.abspath(target_path)
    template_path = templates.project_root.get_path()
    create_file_from_template(template_path, target_path, 'README.rst', context)


def create_gitignore(target_path):
    """Create .gitignore file at the root of the test project

    :param target_path: The path to the outer directory where the package directory is
        contained
    """
    target_path = os.path.abspath(target_path)
    source_path = templates.project_root.get_path()
    shutil.copy(os.path.join(source_path, 'gitignore.j2'), os.path.join(target_path, '.gitignore'))


def create_package_directory(target_path, package_name):
    """Creates package directory for test project

    :param target_path: The path to the outer directory where initialize was called
    :param package_name: The desired name of the package

    :return: Path to created package directory
    """
    return create_directory(os.path.abspath(target_path), package_name)


# Package Root

def create_package_root_modules(target_path, context):
    """Creates __main__.py, __init__.py, and data.py modules for test package

    :param target_path: The path to the test package directory
    :param context: Jinja context used to render template
    """
    template_modules = [
        '__main__.py',
        'data.py',
    ]
    target_path = os.path.abspath(target_path)
    template_path = templates.package_root.get_path()
    # Create template modules
    for template_module in template_modules:
        create_file_from_template(template_path, target_path, template_module, context)
    # Create __init__.py
    create_init(target_path)


def create_test_directories(target_path):
    """Creates base directories for test writing that are initially empty.

    As of version 2.2.0, this method only creates the pages/ directory.

    :param target_path: The path to the test package directory
    """
    target_path = os.path.abspath(target_path)
    dir_path = create_directory(target_path, 'pages')
    create_init(dir_path)


def create_output_directories(target_path, gitignore_files=True):
    """Creates log/ and screenshot/ directories and their .gitignore files

    :param target_path: The path to the test package directory
    :param gitignore_files: (Default = True) Copy template .gitignore files to log/
        and screenshot/ directories if True
    """
    target_path = os.path.abspath(target_path)
    source_path = templates.log.get_path()
    output_directories = [
        'log',
        'screenshot'
    ]
    for directory in output_directories:
        directory_path = create_directory(target_path, directory)
        if gitignore_files:
            # .gitignore files are the same between directories
            shutil.copy(os.path.join(source_path, 'gitignore.j2'), os.path.join(directory_path, '.gitignore'))


def create_tests_init(target_path, context):
    """Creates test package tests/ subdirectory and tests/__init__.py

    :param target_path: The path to the test package directory
    :param context: Jinja context used to render template
    """
    target_path = create_directory(os.path.abspath(target_path), 'tests')
    template_path = templates.tests.get_path()
    create_file_from_template(template_path, target_path, '__init__.py', context)


def create_config_files(target_path, context):
    """Creates test package config directory and config files

    :param target_path: The path to the test package directory
    :param context: Jinja context used to render template
    """
    target_path = create_directory(os.path.abspath(target_path), 'config')
    template_path = templates.config.get_path()
    template_files = [
        '__init__.py',
        'browser.py',
        'browserstack.py',
        'projectfiles.py',
        'site.py',
        'test.py',
        'webdriver.py',
    ]
    for template_file in template_files:
        create_file_from_template(template_path, target_path, template_file, context)


# Helper functions

def create_init(target_path):
    """Create an empty __init__.py file in the target path

    :param target_path: The path to the directory that will contain the new __init__.py
        file
    """
    # "Touch" __init__.py to create an empty file
    init_path = os.path.join(target_path, '__init__.py')
    touch(init_path)


def generate_context(test_package, project_title=None, version_badge=True):
    """Returns a jinja context to use for rendering templates

    :param test_package: Name of the python test package
    :param project_title: (Default = test_package) Human-readable title for the test
        project. Defaults to the value of test_package if not provided
    :param version_badge: (Default = True) Include "generated using
        webdriver_test_tools <version>" badge on README if True

    :return: Dictionary to use as a context when rendering Jinja templates
    """
    if project_title is None:
        project_title = test_package

    context = {
            'test_package': test_package,
            'test_tools_version': __version__,
            'selenium_version': __selenium__,
            'project_title': project_title,
            'version_badge': version_badge,
            }
    return context


def initialize(target_path, package_name, project_title, gitignore_files=True, readme_file=True):
    """Initializes new project package

    This method assumes parameters have been validated. :func:`main()
    <webdriver_test_tools.cmd.init.main()>` handles input validation
    before calling this function

    :param target_path: Path to directory that will contain test package
    :param package_name: Name of the test package to create (will be validated)
    :param project_title: Human readable title of the test project.
    :param gitignore_files: (Default = True) Copy template .gitignore file to
        project root directory if True
    :param readme_file: (Default = True) Render template README file to project
        root directory if True
    """
    outer_path = os.path.abspath(target_path)
    context = generate_context(package_name, project_title)
    # Initialize files in the outer directory
    create_setup_file(outer_path, context)
    if readme_file:
        create_readme(outer_path, context)
    if gitignore_files:
        create_gitignore(outer_path)
    package_path = create_package_directory(outer_path, package_name)
    # Initialize package files
    create_package_root_modules(package_path, context)
    create_test_directories(package_path)
    create_output_directories(package_path, gitignore_files)
    create_tests_init(package_path, context)
    create_config_files(package_path, context)
