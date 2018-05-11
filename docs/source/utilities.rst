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

.. code-block:: python
    :caption: util_example/pages/contact.py

    from webdriver_test_tools.pageobject import BasePage
    from webdriver_test_tools.pageobject.prototypes import FormObject, ModalObject
    from webdriver_test_tools.webdriver import actions, locate
    from selenium.webdriver.common.by import By


    class ContactPage(FormObject):
        # Relative to SiteConfig.BASE_URL
        PAGE_FILENAME = 'contact.html'

        class Locator:
            CONTACT_FORM = (By.ID, 'contact-form')
            SUBMIT = (By.CSS_SELECTOR, 'button[type="submit"]')

        # Attributes used by FormObject methods
        FORM_LOCATOR = Locator.CONTACT_FORM
        SUBMIT_LOCATOR = Locator.SUBMIT
        SUBMIT_SUCCESS_CLASS = SuccessModal

        class Input:
            FIRST_NAME = 'firstname'
            LAST_NAME = 'lastname'
            EMAIL = 'email'
            MESSAGE = 'message'


    class SuccessModal(ModalObject):

        class Locator:
            SUCCESS_MODAL = (By.ID, 'success-modal')
            CLOSE_BUTTON = (By.ID, 'close')

        # Attributes used by ModalObject methods
        MODAL_LOCATOR = Locator.SUCCESS_MODAL
        CLOSE_LOCATOR = Locator.CLOSE_BUTTON


.. todo: Lead in to next example 


Test Data Generation
--------------------

.. todo generate random user info and placeholder text

Example
~~~~~~~

.. todo explain example code

.. code-block:: python
    :caption: util_example/tests/contact.py

    import webdriver_test_tools
    from webdriver_test_tools.testcase import *
    from util_example import config
    from selenium import webdriver

    from util_example.pages.contact import ContactPage

    # Test Case Classes

    class ContactTestCase(WebDriverTestCase):
        """Tests for the Contact Us page"""

        # URL to go to at the start of each test
        SITE_URL = config.SiteConfig.BASE_URL + ContactPage.PAGE_FILENAME

        # Helper Functions

        def generate_contact_form_data(self):
            """Returns a dictionary mapping input names to generated user data"""
            user = data.RandomUser({'nat': 'us'})
            msg = data.loremipsum.generate(1, 'short')
            form_data = {
                ContactPage.Input.FIRST_NAME: user.get_first_name(),
                ContactPage.Input.LAST_NAME: user.get_last_name(),
                ContactPage.Input.EMAIL: user.get_email(),
                ContactPage.Input.MESSAGE: msg,
            }
            return form_data

        # Test Functions

        def test_contact_form(self):
            """Send message through contact form"""

            with self.subTest('Fill all required fields'):
                contact_page.fill_form(contact_form_data)
                # Assert submit is enabled after filling required fields
                self.assertEnabled(contact_page.SUBMIT_LOCATOR)

            with self.subTest('Submit contact form'):
                # click_submit() returns a SuccessModal page object
                success_modal = contact_page.click_submit()
                # Assert success modal is visible on submit
                self.assertVisible(success_modal.MODAL_LOCATOR)

            with self.subTest('Close success modal'):
                success_modal.click_close_button()
                # Assert success modal is no longer visible
                self.assertInvisible(success_modal.MODAL_LOCATOR)


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

