#!/usr/bin/env python3
import os


"""Combine files from docs/souce/ into single README at project root"""

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
    # Only include one table of contents
    toc_added = False
    for filename in doc_files:
        doc_file_path = os.path.join(docs_path, filename)
        with open(doc_file_path) as doc_file:
            for line in doc_file:
                if '.. contents::' in line:
                    # Skip this line if contents was already added
                    if toc_added:
                        continue
                    # Otherwise add set toc_added to True and finish iteration
                    else:
                        toc_added = True
                readme.write(line)
        # Add whitespace between docs
        readme.write('\n\n')


