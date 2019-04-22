
class SiteConfig:
    """Basic class for SiteConfig. Since this is specific to a project, this
    particular class isn't implemented, but exists to define an interface for
    the 2 variables that need to be declared in SiteConfig.

    :var SiteConfig.SITE_URL: URL of the home page
    :var SiteConfig.BASE_URL: Base URL for site pages (followed by a '/')
    """
    SITE_URL = ''
    BASE_URL = ''

    @classmethod
    def parse_relative_url_dict(cls, url_dict):
        """Takes a URL dictionary and returns a full URL based on the values.
        Used to parse :ref:`YAML URL dictionaries <yaml-relative-urls>`

        :param url_dict: A dictionary with the following keys:

            * 'path': The path to a page, relative ot the ``SiteConfig``
              attribute specified in 'relative_to'
            * 'relative_to': A valid attribute in the ``SiteConfig`` class to
              use as a base URL. If the value of that attribute does not have a
              trailing '/', one will be added before appending the value of
              'path'

        :return: A full URL based on the values of the URL dictionary

        :raises ValueError: if ``url_dict['relative_to']`` is not a valid
            attribute name in this class
        :raises KeyError: if 'path' or 'relative_to' are not keys in
            ``url_dict``
        """
        relative_to = url_dict['relative_to']
        try:
            base_url = getattr(cls, relative_to)
        except AttributeError as e:
            error_msg = "Invalid URL 'relative_to' value (relative_to: {}). ".format(relative_to)
            error_msg += 'Must be a valid attribute declared in SiteConfig class'
            raise ValueError(error_msg)
        # Append a '/' if not present
        if not base_url.endswith('/'):
            base_url += '/'
        return base_url + url_dict['path']


