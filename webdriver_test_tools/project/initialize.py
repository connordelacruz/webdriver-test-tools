# Used to create a new test package

import glob
import os
import shutil
import jinja2

import webdriver_test_tools.templates


def create_directories(target_path):
    target_path = os.path.abspath(target_path)
    project_dirs = [
            'config',
            'data',
            'pages',
            'tests',
            'templates',
            ]
    for project_dir in project_dirs:
        path = os.path.join(target_path, project_dir)
        if not os.path.exists(path):
            os.makedirs(path)


def create_config_files(target_path):
    target_path = os.path.abspath(target_path)
    config_path = os.path.dirname(os.path.abspath(webdriver_test_tools.templates.config.__file__))
    # Get only .py files
    config_files = [os.path.basename(file) for file in glob.glob(os.path.join(config_path, '*.py'))]
    for config_file in config_files:
        source_file = os.path.join(config_path, config_file)
        # Precautionary check that this is a file
        if os.path.isfile(source_file):
            target_file = os.path.join(target_path, config_file)
            shutil.copy(source_file, target_file)


def create_template_files(target_path, context):
    target_path = os.path.abspath(target_path)
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
    with open(test_case_target, 'w') as f:
        file_contents = render_template(test_case_template, context)
        f.write(file_contents)


def render_template(template_path, context):
    path, filename = os.path.split(template_path)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(context)


# TODO: update as more templates are created
def generate_context(test_package):
    context = {
            'test_package': test_package
            }
    return context


# TODO: create README?

# TODO: add main
