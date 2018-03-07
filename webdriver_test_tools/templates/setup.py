#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
        name='{{ test_package }}',
        version='0.1.0',
        packages=find_packages(),
        install_requires=[
            'webdriver-test-tools>={{ test_tools_version }}',
            ])
