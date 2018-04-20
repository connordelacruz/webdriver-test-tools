#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
        name='framework_tests',
        version='0.1.0',
        packages=find_packages(),
        install_requires=[
            'webdriver-test-tools>=0.22.0',
            'selenium>=3.11.0',
            ])