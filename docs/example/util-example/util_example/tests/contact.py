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
            'firstname': user.get_first_name(),
            'lastname': user.get_last_name(),
            'email': user.get_email(),
            'message': msg,
        }
        return form_data

    # Test Functions

    def test_contact_form(self):
        """Send message through contact form"""
        # Initialize ContactPage form object
        contact_page = ContactPage(self.driver)
        # Generate form data
        # NOTE: We'll write generate_contact_form_data() in the following section
        contact_form_data = self.generate_contact_form_data()

        # Fill all required fields
        contact_page.fill_inputs(contact_form_data)
        # Assert submit is enabled after filling required fields
        # NOTE: SUBMIT_LOCATOR is set based on the 'submit_locator' value in contact.yml
        self.assertEnabled(contact_page.SUBMIT_LOCATOR,
                           msg='Submit was disabled after filling form inputs')

        # Submit contact form
        # NOTE: click_submit() returns an instance of SUBMIT_SUCCESS_CLASS
        # (which we set to SuccessModal)
        success_modal = contact_page.click_submit()
        # Assert success modal is visible on submit
        # NOTE: MODAL_LOCATOR is set based on the 'modal_locator' value in success_modal.yml
        self.assertVisible(success_modal.MODAL_LOCATOR,
                           msg='Success modal was not visible after clicking submit')

        # Close success modal
        success_modal.click_close_button()
        # Assert success modal is no longer visible
        self.assertInvisible(success_modal.MODAL_LOCATOR,
                             msg='Success modal still visible after clicking close button')

