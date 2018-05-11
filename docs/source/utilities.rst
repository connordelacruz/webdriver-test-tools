Testing Utilities
=================

.. contents::


Page Object Prototypes
----------------------

The ``webdriver_test_tools`` package includes pre-defined subclasses of
:class:`BasePage` for common components like forms and navbars. These classes
define common methods and attributes to reduce the amount of code needed to
create page objects.

For more information and a list of currently implemented page object 
prototypes, see the :doc:`full documentation
</webdriver_test_tools.classes.page_object_prototypes>`.


Example
~~~~~~~

Suppose we have a "Contact Us" form with form validation that disables the
submit button until required inputs are filled. When submit is clicked, a modal
appears informing the user that their submission was successful. The modal has a
close button that hides the modal when clicked.

To test the form submission process, we'll need to have page objects for the
contact form and the success modal, as well as functions for filling out the
form inputs, submitting the form and getting the success modal page object, and
clicking the close button on the modal. To save time writing tests, we can use 
the :class:`FormObject` and :class:`ModalObject` classes, which have pre-defined
methods for most of the tasks we want them to do.

.. todo: explain in a little more detail

.. literalinclude:: ../example/util-example/util_example/pages/contact.py
    :caption: pages/contact.py

.. todo: explain methods

.. literalinclude:: ../example/util-example/util_example/tests/contact.py
    :caption: tests/contact.py
    :pyobject: ContactTestCase.test_contact_form
    
.. todo: Lead in to next example 


Test Data Generation
--------------------

.. todo generate random user info and placeholder text

Example
~~~~~~~

.. todo explain example code

.. literalinclude:: ../example/util-example/util_example/tests/contact.py
    :caption: tests/contact.py
    :pyobject: ContactTestCase.generate_contact_form_data


Screenshots
-----------

The :meth:`WebDriverTestCase.screenshotOnFail()` decorator method can be used to
save screenshots when a test assertion fails. This can be particularly useful
when running tests using :ref:`headless browsers <headless-browsers>`.

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
    <WebDriverTestCase.screenshotOnFail()>` for more information.

