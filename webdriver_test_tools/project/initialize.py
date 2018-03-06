# Used to create a new test package

import webdriver_test_tools
import os, shutil


def create_directories(target_path):
    target_path = os.path.abspath(target_path)
    project_dirs = [
            'config',
            'data',
            'pages',
            'tests',
            'log',
            'templates',
            ]
    for project_dir in project_dirs:
        path = os.path.join(target_path, project_dir)
        if not os.path.exists(path):
            os.makedirs(path)


# TODO: copy default configs
def create_config_files(target_path):
    target_path = os.path.abspath(target_path)
    template_path = os.path.dirname(os.path.abspath(webdriver_test_tools.config.templates.__file__))
    # TODO: iterate files and copy over if they don't exist in new config path

# TODO: create README?

# TODO: add main
