from urllib.parse import urlparse

# TODO: module docstring


def get_base_url(url):
    """Strips query string from a url and returns just the base url

    :param url: The full url to get the base url from

    :return: The url with any query string removed
    """
    current = urlparse(url)
    return current.scheme + '://' + current.netloc + current.path

