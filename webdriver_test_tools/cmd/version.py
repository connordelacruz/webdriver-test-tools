from webdriver_test_tools.__about__ import __version__

def main():
    print('webdriver_test_tools ' + get_version())

def get_version():
    return __version__
