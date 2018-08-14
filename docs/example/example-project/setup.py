#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='example_package',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'webdriver-test-tools>=1.7.1',
        'selenium>=3.11.0',
    ])