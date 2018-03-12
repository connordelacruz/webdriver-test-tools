# Test Projects

## Installation

To initialize a test project, change into the desired directory and run:

```
python -m webdriver_test_tools --init
```

After initializing the test project, run:

```
pip install -e .
```

Installing with the `-e` flag will update the package automatically when changes are made to the source code.

**Note:** Command may be `pip3` instead of `pip` depending on the system

## Basic Command Line Usage

For info on command line arguments:

```
python -m <test_package> --help
```

To run all tests:

```
python -m <test_package>
```

To run all test cases in a file:

```
python -m <test_package> --module <module_name>
```

To run a single TestCase class in a file:

```
python -m <test_package> --module <module_name> --test <TestCaseClassName>
```

To run just one test function in a TestCase class:

```
python -m <test_package> --module <module_name> --test <TestCaseClassName>.<test_function_name>
```

The `--module` argument can be omitted when using the `--test` argument:

```
python -m <test_package> --module <module_name> --test <TestCaseClassName>
```

```
python -m <test_package> --module <module_name> --test <TestCaseClassName>.<test_function_name>
```

**Note:** This can be less efficient as each module will be searched for the specified test, but the difference in performance will likely be unnoticeable.  

To do any of the above in a specific browser rather than running in all available browsers, use the `--browser <browser>` command line argument. For a list of options you can specify with `--browser`, run `python -m <test_package> --help`.

**Note:** Command may be `python3` instead of `python` depending on the system

## Project Structure

`python -m webdriver_test_tools --init` will create the following files and directories:

```
<project-directory>/
├── README.md
├── setup.py
└── <test_package>/
    ├── __main__.py
    ├── config/
    │   ├── __init__.py
    │   ├── site.py
    │   └── test.py
    ├── data/
    ├── pages/
    ├── templates/
    │   ├── page_object.py
    │   └── test_case.py
    └── tests/
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

