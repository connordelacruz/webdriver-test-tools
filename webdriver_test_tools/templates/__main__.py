#!/usr/bin/env python3

import webdriver_test_tools
from {{test_package}} import config, tests


if __name__ == '__main__':
    webdriver_test_tools.test_module.main(tests, config.TestSuiteConfig)
