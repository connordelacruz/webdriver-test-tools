from selenium.webdriver.common.by import By
from webdriver_test_tools.pageobject import *
from webdriver_test_tools.webdriver import actions, locate


class HomePage(BasePage):

    class Locator:
        """WebDriver locator tuples for any elements that will need to be accessed by
        this page object.
        """
        HEADING = (By.TAG_NAME, 'h1')
        INFO_LINK = locate.by_element_text('More information', 'a')

    # Page Methods

    def get_heading_text(self):
        heading_element = self.find_element(self.Locator.HEADING)
        return heading_element.text

    def click_more_information_link(self):
        link_element = self.find_element(self.Locator.INFO_LINK)
        link_element.click()

