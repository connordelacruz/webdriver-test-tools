#!/usr/bin/env python3

from webdriver_test_tools.project import test_module
from test_project import config, tests


if __name__ == '__main__':
    test_module.main(tests, config)