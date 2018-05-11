Testing Utilities
=================

.. contents::


Page Object Prototypes
----------------------

The ``webdriver_test_tools`` package includes pre-defined subclasses of
:class:`BasePage <webdriver_test_tools.pageobject.base.BasePage>` for common
components like forms and navbars. These classes define common methods and
attributes to reduce the amount of code needed to create page objects.

For more information and a list of currently implemented page object 
prototypes, see the :doc:`full documentation
<webdriver_test_tools.pageobject.prototypes>`.


Example
~~~~~~~

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

To save time writing tests, we can use the :mod:`FormObject
<webdriver_test_tools.pageobject.form>` and :mod:`ModalObject
<webdriver_test_tools.pageobject.modal>` classes, which have pre-defined methods
for most of the tasks we want them to do.

.. literalinclude:: ../example/util-example/util_example/pages/contact.py
    :caption: pages/contact.py

The ``FormObject`` attributes ``FORM_LOCATOR`` and ``SUBMIT_LOCATOR`` need to be
set to use the methods ``fill_form()`` and ``click_submit()``.  If the
``SUBMIT_SUCCESS_CLASS`` attribute is set, ``click_submit()`` will return an
initialized page object of that type. The ``ModalObject`` attribute and
``CLOSE_LOCATOR`` needs to be set to use the method ``click_close_button()``. 

After creating those page object classes, we have everything necessary to
write our test in ``ContactTestCase``:

.. literalinclude:: ../example/util-example/util_example/tests/contact.py
    :caption: tests/contact.py
    :pyobject: ContactTestCase.test_contact_form
    
The :meth:`fill_form()
<webdriver_test_tools.pageobject.form.FormObject.fill_form>` method takes a
dictionary mapping input names to the values to set them to. In the following
section, we will create the ``generate_contact_form_data()`` method used to
assign ``contact_form_data`` in the above example.


Test Data Generation
--------------------

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
~~~~~~~

Continuing from the above example, we'll add the following method to
``ContactTestCase``:

.. literalinclude:: ../example/util-example/util_example/tests/contact.py
    :caption: tests/contact.py
    :pyobject: ContactTestCase.generate_contact_form_data

This method generates random user info and message text and returns a dictionary
mapping form input names to the corresponding values.


Screenshots
-----------

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

