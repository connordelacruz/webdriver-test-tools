from webdriver_test_tools.pageobject import utils, BasePage, YAMLParsingPageObject


# TODO: update docs (include YAML_FILE)
class WebPageObject(YAMLParsingPageObject):
    """Page object prototype for web pages

    :var WebPageObject.PAGE_FILENAME: File name of the page relative to a base
        URL declared in ``SiteConfig``
    :var WebPageObject.PAGE_URL: Full URL of the page (e.g.
        ``SiteConfig.BASE_URL + PAGE_FILENAME``)
    """
    _YAML_ROOT_KEY = 'web_page'

    # TODO: doc and implement
    SITE_CONFIG = None
    # TODO: rename to PAGE_RELATIVE_PATH?
    PAGE_FILENAME = None
    PAGE_URL = None

    def parse_yaml(self, file_path):
        """Parse a YAML representation of the web page object and set
        attributes accordingly

        See :ref:`YAML WebPageObjects doc <yaml-web-page-objects>` for details
        on syntax.

        :param file_path: Full path to the YAML file
        """
        parsed_yaml = super().parse_yaml(file_path)
        # Initialize locators
        try:
            url = parsed_yaml['url']
            if isinstance(url, str):
                # TODO: what about PAGE_FILENAME?
                self.PAGE_URL = url
            # TODO: if dict, set attributes accordingly
            elif isinstance(url, dict):
                # TODO: key error if either is missing
                self.PAGE_FILENAME = url['path']
                # TODO: figure out a way to get project config (self.SITE_CONFIG)
                relative_to = url['relative_to']
            else:
                error_msg = "Invalid 'url' value (url: {}). ".format(url)
                error_msg += "Must be a string or a dictionary with keys 'path' and 'relative_to'"
                raise utils.yaml.YAMLValueError(error_msg)
        except KeyError as e:
            raise utils.yaml.YAMLKeyError(
                'Missing required {} key in modal YAML'.format(e)
            )

    def get_page_title(self):
        """Get the title of the current page

        :return: Title of the current page
        """
        return self.driver.get_title()

