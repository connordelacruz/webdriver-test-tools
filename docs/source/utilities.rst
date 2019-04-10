=================
Testing Utilities
=================

.. contents::


Page Object Prototypes
======================

The ``webdriver_test_tools`` package includes pre-defined subclasses of
:class:`BasePage <webdriver_test_tools.pageobject.base.BasePage>` for common
components like forms and navbars. These classes define common methods and
attributes to reduce the amount of code needed to create page objects.

For more information and a list of currently implemented page object 
prototypes, see the :doc:`full documentation
<webdriver_test_tools.pageobject.prototypes>`.


Example
-------

Suppose we have a "Contact Us" form with form validation that disables the
submit button until required inputs are filled. When submit is clicked, a modal
appears informing the user that their submission was successful. The modal has a
close button that hides the modal when clicked.

To test the form submission process, we'll need to have page objects for the
contact form and the success modal, as well as functions for filling out the
form inputs, submitting the form and getting the success modal page object, and
clicking the close button on the modal. We'll need to create
``pages/contact.py`` with ``ContactPage`` and ``SuccessModal`` page object
classes for the "Contact Us" page and submission success modal respectively.
We'll then need to create ``tests/contact.py`` with test class
``ContactTestCase``.

To save time writing tests, we can use the :mod:`prototypes.FormObject
<webdriver_test_tools.pageobject.form>` and :mod:`prototypes.ModalObject
<webdriver_test_tools.pageobject.modal>` classes, which have pre-defined methods
for most of the tasks we want them to do.

.. literalinclude:: ../example/util-example/util_example/pages/contact.py
    :caption: pages/contact.py

.. todo Better phrasing and more detail

The ``FormObject`` parses the file specified with the ``YAML_FILE`` attribute on
initialization:

.. literalinclude:: ../example/util-example/util_example/pages/contact.yml
    :caption: pages/contact.yml

This is used to set the attributes ``FORM_LOCATOR`` and ``SUBMIT_LOCATOR``,
which are required to use the methods ``fill_inputs()`` and ``click_submit()``.
If the ``SUBMIT_SUCCESS_CLASS`` attribute is set, ``click_submit()`` will return
an initialized page object of that type. 

.. note::

   For more information on YAML syntax, see :ref:`yaml-page-objects`.

The ``ModalObject`` attribute ``CLOSE_LOCATOR`` needs to be set to use the
method ``click_close_button()``. 

After creating those page object classes, we have everything necessary to
write our test in ``ContactTestCase``:

.. literalinclude:: ../example/util-example/util_example/tests/contact.py
    :caption: tests/contact.py
    :pyobject: ContactTestCase.test_contact_form
    
The :meth:`fill_inputs()
<webdriver_test_tools.pageobject.form.FormObject.fill_inputs>` method takes a
dictionary mapping input names to the values to set them to. In the `Test Data
Generation`_ section, we will create the ``generate_contact_form_data()`` method
used to assign ``contact_form_data`` in the above example.


Using Prototypes in New Page Objects
------------------------------------

.. todo rephrase title?

By default, page objects generated using the ``new page`` command use a basic
template and subclass :class:`BasePage
<webdriver_test_tools.pageobject.base.BasePage>`. You can specify a page object
prototype to use as a basis for a new page using the ``--prototype`` (or ``-p``)
argument:

::

   python -m <test_package> new page <module_name> <PageObjectClass> -p <prototype>

Where ``<prototype>`` is one of the options listed when calling ``python -m
<test_package> new page --help``:

::

   ...
     -p <prototype_choice>, --prototype <prototype_choice>
                           Page object prototype to subclass.
                           Options: {form,modal,nav,"collapsible nav","web page"}
   ...

The generated page object will subclass the corresponding prototype class and
include any variable declarations used by that prototype's methods.


Test Data Generation
====================

The ``webdriver_test_tools`` package includes some utility packages for
generating random user information and placeholder text to use for sample data:

    - `randomuser <https://pypi.org/project/randomuser/>`__
    - `py-loremipsum <https://pypi.org/project/py-loremipsum/>`__

The :class:`RandomUser <randomuser.RandomUser>` class generates fake user
information (names, emails, contact info, addresses, etc). The :mod:`loremipsum`
module generates `lorem ipsum <https://en.wikipedia.org/wiki/Lorem_ipsum>`__
placeholder text.

These utilities are imported in the :mod:`webdriver_test_tools.data` module for
convenience. To use them, add the following import statement:

.. code-block:: python

    from webdriver_test_tools import data


Example
-------

Continuing from the above example, we'll add the following method to
``ContactTestCase``:

.. literalinclude:: ../example/util-example/util_example/tests/contact.py
    :caption: tests/contact.py
    :pyobject: ContactTestCase.generate_contact_form_data

This method generates random user info and message text and returns a dictionary
mapping form input names to the corresponding values.


Static Test Data
================

Some tests may require static data for testing (e.g. login info for a registered
user). These values can be stored in inside the ``<test_package>/data.py``
module to keep them independent of test modules or page objects.


Example
-------

Suppose we have a user registration form that displays an error when registering
with an email of an existing user. To test this functionality, we'll need to use
an email that we know is already registered. We can add the following value to
the ``data`` module and import it in our test modules:

.. literalinclude:: ../example/util-example/util_example/data.py
    :caption: data.py

We can then import it in our test cases. Since this data is independent of our
test cases, it can be easily used in other tests (e.g. testing a sign in page).
Additionally, if the registered user email changes at any point, it can be
updated in a single place without altering the tests.


Screenshots
===========

The :meth:`WebDriverTestCase.screenshotOnFail()
<webdriver_test_tools.testcase.webdriver.WebDriverTestCase.screenshotOnFail>`
decorator method can be used to save screenshots when a test assertion fails.
This can be particularly useful when running tests using :ref:`headless browsers
<headless-browsers>`.

.. code-block:: python
    :caption: Usage example:

    class ExampleTestCase(WebDriverTestCase):
        ...
        @WebDriverTestCase.screenshotOnFail()
        def test_method(self):
            ...

Screenshots are saved to the directory configured in
``WebDriverConfig.SCREENSHOT_PATH``, which is set to
``<test_package>/screenshot/`` by default.

.. note::

    Currently, this method does not take a screenshot for assertions that fail
    within a subTest. See the :meth:`method's documentation
    <webdriver_test_tools.testcase.webdriver.WebDriverTestCase.screenshotOnFail>`
    for more information.

