import os

from setuptools import setup, find_packages

def readme():
    with open('README.rst') as f:
        return f.read()

def get_package_data():
    template_root = 'project/templates/'
    template_dirs = [
        'config',
        'log',
        'package_root',
        'project_root',
        'templates',
        'templates/page_object',
        'tests',
    ]
    # Get .j2 template files
    template_data = [
        template_root + template_dir + '/*.j2' for template_dir in template_dirs
    ]
    return {
        'webdriver_test_tools': template_data,
    }


# Get metadata
base_path = os.path.dirname(__file__)
about = {}
with open(os.path.join(base_path, 'webdriver_test_tools', '__about__.py')) as f:
    exec(f.read(), about)


# Installation

install_requires = [
    'selenium>={}'.format(about['__selenium__']),
    'colour-runner>=0.1.1,<0.2',
    'randomuser>=1.5.1,<1.6',
    'py-loremipsum>=1.0.0',
    'Jinja2>=2.10',
    'urllib3>=1.22',
    'blessings>=1.6.1',
    'PyYAML>=5.1,<5.2',
]

entry_points = {
    'console_scripts': [
        'webdriver_test_tools = webdriver_test_tools.__main__:main',
        'wtt = webdriver_test_tools.__main__:main',
    ]
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
'''.format(about['__devstatus__'])

project_urls = {
    'Documentation': about['__documentation__'],
    'Source': about['__url__'],
}


setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__summary__'],
    long_description=readme(),
    url=about['__url__'],
    download_url=about['__download__'],
    project_urls=project_urls,
    author=about['__author__'],
    author_email=about['__email__'],
    license=about['__license__'],
    classifiers=[x for x in CLASSIFIERS.split("\n") if x],
    packages=find_packages(),
    include_package_data=True,
    package_data=get_package_data(),
    entry_points=entry_points,
    install_requires=install_requires,
)
