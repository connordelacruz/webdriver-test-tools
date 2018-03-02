#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
        name='webdriver_test_tools',
        version='0.1.0',
        packages=find_packages(),
        install_requires=[
            'selenium>=3.9',
            'colour-runner>=0.0.5'
            ])
