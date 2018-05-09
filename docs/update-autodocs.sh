#!/usr/bin/env bash

sphinx-apidoc $@ -eM -o source/ ../webdriver_test_tools/ ..webdriver_test_tools/log/ ../webdriver_test_tools/project/templates/
