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
        contact_page = ContactPage(self.driver)
        contact_form_data = self.generate_contact_form_data()

        with self.subTest('Fill all required fields'):
            contact_page.fill_inputs(contact_form_data)
            # Assert submit is enabled after filling required fields
            # (SUBMIT_LOCATOR is set based on the submit_locator value in contact.yml)
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

