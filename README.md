# Selenium WebDriver Test Framework

Utilities for writing front-end test suites using Selenium WebDriver and python unit tests.

## TODO:

* Link to relevant documentation for Selenium WebDriver, python unittest library

## Overview

This project aims to reduce the amount of time and additional code required to automate front-end functional testing by providing utilities and conventions for building test suites.

## Prerequisites

### python

* python 3+
* pip

### drivers

* [geckodriver](https://github.com/mozilla/geckodriver/releases) (FireFox)
* [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) (Google Chrome)

On MacOS, both drivers can be installed using [Homebrew](https://brew.sh/):

```
brew install geckodriver chromedriver
```

Support for more browser drivers will be added in future updates.

## Installation

After installing the above prerequisites, run:

```
pip install webdriver-test-tools
```

**Note:** Command may be `pip3` instead of `pip` depending on the system

## Command Line Usage

For info on command line arguments:

```
webdriver_test_tools --help
```

To initialize a new test project in the current directory:

```
webdriver_test_tools --init
```

This will generate a new test package with template files and project directories.


**Note:** Command may be `python3` instead of `python` depending on the system





