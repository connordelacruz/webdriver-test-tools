# Used to create a new test package

import webdriver_test_tools.templates
import os, glob, shutil


def create_directories(target_path):
    target_path = os.path.abspath(target_path)
    project_dirs = [
            'config',
            'data',
            'pages',
            'tests',
            # 'log', # TODO: no longer using log/
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

# TODO: create README?

# TODO: add main
