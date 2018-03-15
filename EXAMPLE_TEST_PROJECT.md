# Test Project Example

## WORK IN PROGRESS

This documentation is currently a work in progress and is missing some sections.  

---

## Initialize the project

First, create a directory for the test project:

```
mkdir example-project
cd example-project
```

Once in the project directory, run the following command to initialize the project:

```
python -m webdriver_test_tools --init
```

You will be prompted to enter a name for the test project python package. To be a valid package name, it needs to only use alphanumeric characters and underscores and it cannot start with a number. For this example, we'll call it `example_package`. Initializing the project should create the following files and directories:

```
example-project/
├── example_package/
│   ├── config/
│   │   ├── __init__.py
│   │   ├── site.py
│   │   └── test.py
│   ├── data/
│   ├── pages/
│   ├── templates/
│   │   ├── page_object.py
│   │   └── test_case.py
│   ├── tests/
│   │   └── __init__.py
│   └── __main__.py
├── README.md
└── setup.py
```

After initializing the test project, run:

```
pip install -e .
```

Installing with the `-e` flag will update the package automatically when changes are made to the source code.

**Note:** Command may be `pip3` instead of `pip` depending on the system.


## Configure site URLs

After initializing a project, the URL of the site to be tested will need to be configured. In `example_package/config/site.py`, set the `SITE_URL` and `BASE_URL` of the `SiteConfig` class. You can add any other URLs you'll need as class variables as well. We'll use [example.com](https://www.example.com/).

`config/site.py`:

```python
# URL configurations for a site

from webdriver_test_tools.config import site


class SiteConfig(site.SiteConfig):
    # URL of the home page
    SITE_URL = 'https://www.example.com'
    # Base URL for site pages (followed by a '/')
    BASE_URL = SITE_URL + '/'
    # DECLARE ANY OTHER URL VARIABLES NEEDED FOR TESTING HERE
```

**TODO:** add additional URL here for testing 'More information...' link (https://www.iana.org/domains/reserved)


## Add a page object

**TODO:** continue from here

**TODO:** add example code


## Add a test

**TODO:** add example code


## Run the test

**TODO:** document and example test output for successful and failed test

