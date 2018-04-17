#!/usr/bin/env python3
import os
from webdriver_test_tools.project import templates
from webdriver_test_tools.project import initialize

"""Rebuild source docs templates that are based on project template files"""

docs_path = os.path.dirname(os.path.abspath(__file__))
target_path = os.path.join(docs_path, 'source/test_projects.rst')
template_path = templates.project_root.get_path()
readme_path = os.path.join(template_path, 'README.rst.j2')

test_package = '<test_package>'
project_title = 'Test Project Overview'

context = initialize.generate_context(test_package=test_package, project_title=project_title, version_badge=False)
initialize.render_template_to_file(readme_path, context, target_path)

