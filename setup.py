#!/usr/bin/env python3

from setuptools import setup, find_packages

# Get __version__
with open('./webdriver_test_tools/version.py') as f:
    exec(f.read())

setup(
        name='webdriver_test_tools',
        version=__version__,
        description='Tools for using Selenium WebDriver with Python unit testing',
        url='https://github.com/connordelacruz/webdriver-test-tools',
        download_url='https://github.com/connordelacruz/webdriver-test-tools/archive/{}.tar.gz'.format(__version__),
        author='Connor de la Cruz',
        author_email='connor.c.delacruz@gmail.com',
        license='MIT',
        packages=find_packages(),
        entry_points={
            'console_scripts': ['webdriver_test_tools = webdriver_test_tools.__main__:main']
        },
        install_requires=[
            'selenium>=3.9',
            'colour-runner>=0.0.5',
            'randomuser>=1.0.0',
            'Jinja2>=2.9.5',
            ]
        )
