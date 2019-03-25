"""Various utility methods for package submodules."""

import re
from urllib.parse import urlparse


def get_base_url(url):
    """Strips query string from a url and returns just the base url

    :param url: The full url to get the base url from

    :return: The url with any query string removed
    """
    current = urlparse(url)
    return current.scheme + '://' + current.netloc + current.path


def validate_filename(filename, allow_spaces=False):
    """Strips invalid characters from a filename

    Considers `POSIX "fully portable filenames"
    <http://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap03.html#tag_03_282>`__
    valid. These include:

        A-Z a-z 0-9 ._-

    Filenames cannot begin with a hyphen.

    :param filename: The desired file name (without path)
    :param allow_spaces: (Default = False) If True, spaces will be considered
        valid characters

    :return: Filename with invalid characters removed
    """
    regex = r'^-|[^\d\w\. -]' if allow_spaces else r'^-|[^\d\w\.-]'
    return re.sub(regex, '', filename)

