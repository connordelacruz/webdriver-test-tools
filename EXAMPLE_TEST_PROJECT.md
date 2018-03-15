# Test Project Example

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

After initializing a project, the URL of the site to be tested will need to be configured. In `example_package/config/site.py`, set the `SITE_URL` and `BASE_URL` of the `SiteConfig` class. You can add any other URLs you'll need as class variables as well. 

**TODO:** add example code


## Add a page object

**TODO:** continue from here

**TODO:** add example code


## Add a test

**TODO:** add example code


## Run the test

**TODO:** document and example test output for successful and failed test

