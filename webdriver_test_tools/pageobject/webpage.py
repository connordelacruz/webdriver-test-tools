from webdriver_test_tools.pageobject import utils, YAMLParsingPageObject


class WebPageObject(YAMLParsingPageObject):
    """Page object prototype for web pages

    Subclasses should set the following attributes:

    :var WebPageObject.YAML_FILE: Path to a YAML file representing the web
        page. This file is parsed during initialization using
        :meth:`parse_yaml` and is used to determine :attr:`PAGE_FILENAME` and
        :attr:`PAGE_URL`
    :var WebPageObject.SITE_CONFIG: Test project's :class:`SiteConfig` class.
        Used in :meth:`parse_yaml` to determine page url attributes if the YAML
        'url' value is a dictionary with a path relative to a configured URL

    The following attributes are determined based on the contents of
    :attr:`YAML_FILE` (or parsed from :attr:`INPUT_DICTS`, which should be set
    in subclasses if :attr:`YAML_FILE` is ``None``):

    :var WebPageObject.PAGE_FILENAME: File name of the page relative to a base
        URL declared in ``SITE_CONFIG`` class.

        .. note::

            If the 'url' key in the YAML file is set to a full URL,
            :attr:`PAGE_FILENAME` will be set to ``None``

    :var WebPageObject.PAGE_URL: Full URL of the page (e.g.
        ``SITE_CONFIG.BASE_URL + PAGE_FILENAME``)
    """
    _YAML_ROOT_KEY = 'web_page'

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
            # url can be a url string or a dict mapping the page path relative
            # to a SITE_CONFIG attribute
            if isinstance(url, str):
                self.PAGE_URL = url
            elif isinstance(url, dict):
                self.PAGE_FILENAME, self.PAGE_URL = self._parse_url_dict(url)
            else:
                error_msg = "Invalid 'url' value (url: {}). ".format(url)
                error_msg += "Must be a string or a dictionary with keys 'path' and 'relative_to'"
                raise utils.yaml.YAMLValueError(error_msg)
        except KeyError as e:
            raise utils.yaml.YAMLKeyError(
                'Missing required {} key in web page YAML'.format(e)
            )

    def _parse_url_dict(self, url):
        """Parse 'url' dictionary in web page YAML

        :param url: 'url' dictionary from parsed YAML. Expected to have keys
            'path' and 'relative_to'

        :return: A tuple containing the relative path to the page and the full
            URL

        :raises YAMLKeyError: if ``url`` is missing either required key
        :raises YAMLValueError: if ``url['relative_to']`` is not a valid
            attribute name of :attr:`SITE_CONFIG` class
        """
        # TODO: what if URL is an exact attribute in site config and not relative?
        try:
            return (
                url['path'],
                self.SITE_CONFIG.parse_relative_url_dict(url)
            )
        except KeyError as e:
            raise utils.yaml.YAMLKeyError(
                "Missing required {} key in web page 'url' dictionary"
            )
        except ValueError as e:
            error_msg = "Invalid URL 'relative_to' value (relative_to: {}). ".format(url['relative_to'])
            error_msg += 'Must be a valid attribute declared in SiteConfig class'
            raise utils.YAMLValueError(error_msg)

    def get_page_title(self):
        """Get the title of the current page

        :return: Title of the current page
        """
        return self.driver.get_title()

