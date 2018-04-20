#!/usr/bin/env python3

from webdriver_test_tools.project import test_module
from framework_tests import config, tests


if __name__ == '__main__':
    test_module.main(tests, config)