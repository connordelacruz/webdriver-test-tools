# Selenium Web Driver Test Framework

## TODO:

* Update instructions now that utilities are a separate package
* Add detailed documentation
* Info on page object model
* Add setup instructions using the BitBucket url instead of a local directory?


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

## Installation

After installing the above prerequisites, change to the root directory of the project and run:

```
pip install -e .
```

Installing with the `-e` flag will update the package automatically when changes are made to the source code.

*Note:* Command may be `pip3` instead of `pip` depending on the system

## Basic Usage

For info on command line arguments:

```
python -m test_package --help
```

To run all tests:

```
python -m test_package
```

To run all test cases in a file:

```
python -m test_package.tests.<module_name>
```

To run a single TestCase class in a file:

```
python -m test_package.tests.<module_name> --test <TestCaseClassName>
```

To run just one test function in a TestCase class:

```
python -m test_package.tests.<module_name> --test <TestCaseClassName>.<test_function_name>
```

To do any of the above in a specific browser rather than running in all available browsers, use the `--browser <browser>` command line argument. For a list of options you can specify with `--browser`, run `python -m test_package --help`.

*Note:* Command may be `python3` instead of `python` depending on the system

## Project Structure

```
test_package
├── config
├── data
├── pages
├── tests
├── templates
└── log
```

### config/

Configurations used by test scripts for site URLs, web driver options, and the python unittest framework.

### data/

Static data for tests that must use specific values (e.g. emails, check-in codes). 

### pages/

Page object classes for pages and components. These classes should handle locating and interacting with elements on the page.

### tests/

Test case modules. These use page objects to interact with elements and assert that the expected behavior occurs.

### templates/

Template files to use as a starting point when writing new test modules or page objects.

### log/

Log output of the web drivers. 





