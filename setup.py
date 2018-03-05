#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
        name='webdriver_test_tools',
        version='0.2.0',
        url='https://github.com/connordelacruz/webdriver-test-tools',
        download_url='https://github.com/connordelacruz/webdriver-test-tools/archive/0.2.0.tar.gz',
        author='Connor de la Cruz',
        author_email='connor.c.delacruz@gmail.com',
        license='MIT',
        packages=find_packages(),
        install_requires=[
            'selenium>=3.9',
            'colour-runner>=0.0.5',
            'randomuser>=0.1.1'
            ]
        )
