# Test Project Example

## WORK IN PROGRESS

This documentation is currently a work in progress and is missing some sections.  

**TODO:** link to example project to see full source code

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


## Configure site URLs

After initializing a project, the URL of the site to be tested will need to be configured. In `example_package/config/site.py`, set the `SITE_URL` and `BASE_URL` of the `SiteConfig` class.  

**TODO:** Briefly explain motiviation for declaring URLs in a single location

For this example, we'll use [example.com](https://www.example.com/).

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

We'll be testing that clicking a link takes us to an external page, so we'll add another variable `INFO_URL` to `SiteConfig`:

`config/site.py`:

```python
...
class SiteConfig(site.SiteConfig):
    ...
    # DECLARE ANY OTHER URL VARIABLES NEEDED FOR TESTING HERE
    # URL linked to by the 'More Information' link on example.com
    INFO_URL = 'https://www.iana.org/domains/reserved'
```


## Add a page object

### Creating a new page object module

This test framework is best used with the [Page Object Model](https://martinfowler.com/bliki/PageObject.html). Interaction with the page should be handled by page objects to minimize the need to alter tests whenever the HTML is changed.

After configuring URLs, we'll want to add a page object for the home page of example.com. Copy the template file `templates/page_object.py` to the `pages/` directory and name the copied file `home.py`:

```
cp example_package/templates/page_object.py example_package/pages/home.py
```

In `pages/home.py`, rename the `TemplatePage` class to `HomePage`. You can also remove the `Input` subclass. It's sometimes useful to keep track of input name attributes, but since there's no inputs on example.com it can be omitted.

### Locating page elements

For any element we need to locate, we'll want to keep track of how to target it in the `Locator` subclass. Selenium WebDriver locators are tuples in the format `(By.<selection type>, <selection string>)`, where `<selection type>` is one of the constants declared in `selenium.webdriver.common.by.By` and `<selection string>` is the string used to find the element.

Example.com is a pretty bare bones website, so these examples will be pretty contrived. We'll add locators for the site heading and the 'More information...' link.

To locate the 'More information...' link, we're going to select it by its link text. Update the `import` statement from the `webdriver_test_tools.webdriver` package to import the `locate` module:

```python
# Page object

# Imports
# ----------------------------------------------------------------
...
from webdriver_test_tools.webdriver import actions, locate 
...
```

Then we'll add `HEADING` and `INFO_LINK` variables to the `Locator` subclass:

```python
...
class HomePage(BasePage):
    class Locator(object):
        """WebDriver locator tuples for any elements that will need to be accessed by
this page object."""
        HEADING = (By.TAG_NAME, 'h1')
        INFO_LINK = locate.by_element_text('More information', 'a')
    ...
```

**TODO:** brief explanation of `locate.by_element_text()`


### Interacting with page elements

For our example tests, we'll want to look at the heading text and click on the 'More information...' link. Add the following functions to the `HomePage` class:

```python
...
class HomePage(BasePage):
    ...
    def get_heading_text(self):
        heading_element = self.driver.find_element(*self.Locator.HEADING)
        return heading_element.text

    def click_more_information_link(self):
        link_element = self.driver.find_element(*self.Locator.INFO_LINK)
        link_element.click()
```

## Add a test

### Creating a new test module

Now that we have a page object for interacting with example.com, we can write a test case. Copy the file `templates/test_case.py` to the `tests/` directory and name the copied file `homepage.py`:

```
cp example_package/templates/test_case.py example_package/tests/homepage.py
```

Whenever a new test module is created, it needs to be imported in `tests/__init__.py` so the framework can detect it when loading tests.

`tests/__init__.py`:

```python
from . import homepage
```

In `tests/homepage.py`, rename the `TemplateTestCase` class to `HomePageTestCase`. Then import the `HomePage` class created in the previous step.

`tests/homepage.py`:

```python
# Imports
# ----------------------------------------------------------------
from example_package.pages.home import HomePage
...
class HomePageTestCase(WebDriverTestCase):
    """Really contrived example test case"""
    ...
```

### Adding test functions

We're going to add 2 test functions: 

1. Retrieve the heading text and assert that it says 'Example Domain'
2. Click the 'More information...' link and assert that the URL matches SiteConfig.INFO_URL

`tests/homepage.py`:

```python
...
class HomePageTestCase(WebDriverTestCase):
    ...
    def test_page_heading(self):
        """Ensure that the page heading text is correct"""
        page_object = HomePage(self.driver)
        heading_text = page_object.get_heading_text()
        self.assertEqual('Example Domain', heading_text)

    def test_more_information_link(self):
        """Test that the 'More information...' link goes to the correct URL"""
        page_object = HomePage(self.driver)
        expected_url = config.SiteConfig.INFO_URL
        page_object.click_more_information_link()
        self.assertTrue(webdriver_test_tools.test.url_change_test(self.driver, expected_url))
```

**Note:** Test functions need to begin with the prefix `test_` in order for the python `unittest` library to recognize them as tests.

We should now have everything we need to run our test suite.

## Run the test

**TODO:** document and example test output for successful and failed test

