from datetime import datetime

__all__ = [
    '__title__', '__project__', '__summary__', '__release__', '__version__', '__devstatus__',
    '__url__', '__documentation__', '__download__', '__selenium__',
    '__author__', '__email__', '__license__', '__copyright__',
]

__title__ = 'webdriver_test_tools'
__project__ = 'WebDriver Test Tools'
__summary__ = 'A front-end testing framework using Selenium WebDriver and Python'

__release__ = '2.5.1-alpha'
__version__ = __release__.split('-')[0]
__devstatus__ = 'Development Status :: 3 - Alpha'

__url__ = 'https://github.com/connordelacruz/webdriver-test-tools/'
__documentation__ = 'https://connordelacruz.com/webdriver-test-tools/'
__download__ = __url__ + 'archive/{}.tar.gz'.format(__version__)

# TODO: look into upgrading
__selenium__ = '3.11.0'

__author__ = 'Connor de la Cruz'
__email__ = 'connor.c.delacruz@gmail.com'

__license__ = 'MIT'
__copyright__ = '{}, {}'.format(datetime.now().year, __author__)
