#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='page_object_tests',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'webdriver-test-tools>=2.6.0',
        'selenium>=3.11.0',
    ])