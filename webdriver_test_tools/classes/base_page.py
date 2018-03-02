# Base class for page objects


class BasePage(object):
    """Base class for page objects"""

    def __init__(self, driver):
        self.driver = driver

    def get_page_title(self):
        return driver.get_title()
