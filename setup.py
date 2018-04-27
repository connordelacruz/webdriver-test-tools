from setuptools import setup, find_packages

def readme():
    with open('README.rst') as f:
        return f.read()

# Get __version__, __devstatus__, and __selenium__
with open('./webdriver_test_tools/version.py') as f:
    exec(f.read())


# Installation

install_requires = [
    'selenium>={}'.format(__selenium__),
    'colour-runner>=0.0.5',
    'randomuser>=1.4.0',
    'py-loremipsum>=1.0.0',
    'Jinja2>=2.9.5',
    'urllib3>=1.22',
    'blessings>=1.6.1',
]

entry_points = {
    'console_scripts': ['webdriver_test_tools = webdriver_test_tools.__main__:main']
}

# Metadata

CLASSIFIERS = '''
Programming Language :: Python
Programming Language :: Python :: 3
Programming Language :: Python :: 3.4
Programming Language :: Python :: 3.5
Programming Language :: Python :: 3.6
Environment :: Console
License :: OSI Approved :: MIT License
Natural Language :: English
Intended Audience :: Developers
Operating System :: MacOS :: MacOS X
Operating System :: Microsoft :: Windows
Topic :: Software Development :: Libraries
Topic :: Software Development :: Testing
Topic :: Software Development :: Quality Assurance
Topic :: Utilities
{}
'''.format(__devstatus__)

url = 'https://github.com/connordelacruz/webdriver-test-tools/'

download_url = url + 'archive/{}.tar.gz'.format(__version__)

project_urls = {
    'Documentation': 'http://connordelacruz.com/webdriver-test-tools/',
    'Source': url,
}


setup(
    name='webdriver_test_tools',
    version=__version__,
    description='A front-end testing framework using Selenium WebDriver and Python',
    long_description=readme(),
    url=url,
    download_url=download_url,
    project_urls=project_urls,
    author='Connor de la Cruz',
    author_email='connor.c.delacruz@gmail.com',
    license='MIT',
    classifiers=[x for x in CLASSIFIERS.split("\n") if x],
    packages=find_packages(),
    entry_points=entry_points,
    install_requires=install_requires,
)
