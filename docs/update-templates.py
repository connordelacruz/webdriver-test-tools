#!/usr/bin/env python3
import os
import webdriver_test_tools.project.templates
from webdriver_test_tools.project import initialize

# TODO: document and clean up

docs_path = os.path.dirname(os.path.abspath(__file__))
target_path = os.path.join(docs_path, 'source/test_projects.rst')
template_path = os.path.dirname(os.path.abspath(webdriver_test_tools.project.templates.__file__))
readme_path = os.path.join(template_path, 'README.rst.j2')

test_package = '<test_package>'
project_title = 'Test Project Overview'

context = initialize.generate_context(test_package=test_package, project_title=project_title, version_badge=False)
initialize.render_template_to_file(readme_path, context, target_path)

