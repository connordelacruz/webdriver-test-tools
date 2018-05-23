#!/usr/bin/env python3
import os


# TODO: handle .. contents:: directives

project_root = os.path.dirname(os.path.abspath(__file__))
readme_path = os.path.join(project_root, 'README.rst')
docs_path = os.path.join(project_root, 'docs', 'source')
doc_files = [
    'README.rst',
    'test_projects.rst',
]

# Move old readme
os.rename(readme_path, readme_path + '.bak')
# Combine doc_files to create readme
with open(readme_path, 'w') as readme:
    for filename in doc_files:
        doc_file_path = os.path.join(docs_path, filename)
        with open(doc_file_path) as doc_file:
            readme.write(doc_file.read())
        # Add transition and whitespace between docs
        readme.write('\n\n----\n\n')


