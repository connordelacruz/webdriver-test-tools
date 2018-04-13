# example_package

## Installation

After initializing the test project, change to the root directory of the project and run:

```
pip install -e .
```

Installing with the `-e` flag will update the package automatically when changes are made to the source code.

*Note:* Command may be `pip3` instead of `pip` depending on the system

### Configuration

After initializing a project, the URL of the site to be tested will need to be configured. In `example_package/config/site.py`, set the `SITE_URL` and `BASE_URL` of the `SiteConfig` class. You can add any other URLs you'll need as class variables as well. 

## Basic Command Line Usage

For info on command line arguments:

```
python -m example_package --help
```

To run all tests:

```
python -m example_package
```

To run all test cases in a file:

```
python -m example_package --module <test_module>
```

Multiple modules can be run at once:

```
python -m <test_package> --module <test_module0> <test_module1>
```

To run a single TestCase class in a file:

```
python -m example_package --module <test_module> --test <TestClass>
```

To run just one test method in a TestCase class:

```
python -m example_package --module <test_module> --test <TestClass>.<test_method>
```

The `--module` argument can be omitted when using the `--test` argument:

```
python -m example_package --test <TestClass>
```

```
python -m example_package --test <TestClass>.<test_method>
```

*Note:* This can be less efficient as each module will be searched for the specified test, but the difference in performance will likely be unnoticeable.  

Multiple test classes and test methods can be run at once:

```
python -m <test_package> --test <TestClass0> <TestClass1>.<test_method>
```

To do any of the above in a specific browser rather than running in all available browsers, use the `--browser <browser>` command line argument. For a list of options you can specify with `--browser`, run `python -m example_package --help`.

*Note:* Command may be `python3` instead of `python` depending on the system

## Project Structure

```
example_package
├── config
├── data
├── pages
├── tests
└── templates
```

This test structure is best used with the [Page Object Model](https://martinfowler.com/bliki/PageObject.html). Interaction with the page should be handled by page objects to minimize the need to alter tests whenever the HTML is changed.

### Test Project Root Contents

`setup.py` is a python package setup file that allows the new test suite to be installed as a pip package.

### Test Package Contents

#### config/

Configurations used by test scripts for site URLs, web driver options, and the python unittest framework.

#### data/

Static data for tests that must use specific values (e.g. emails, check-in codes). 

#### pages/

Page object classes for pages and components. These classes should handle locating and interacting with elements on the page. A template page object can be found in `templates/page_object.py`.

#### tests/

Test case modules. These use page objects to interact with elements and assert that the expected behavior occurs. A template test file can be found in `templates/test_case.py`.

When adding new test files, be sure to update `tests/__init__.py` to include the new module so the framework can detect the new test cases.

#### templates/

Template files to use as a starting point when writing new test modules or page objects.

---

![webdriver_test_tools 0.15.1](https://img.shields.io/badge/generated%20using-webdriver__test__tools%200.15.1-blue.svg?style=for-the-badge)