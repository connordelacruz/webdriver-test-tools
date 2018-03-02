# Configurations for webdriver

# TODO: make independent from Nationals package

from selenium import webdriver
import selenium_aem_nationals
import os.path

# Variables
# ----------------------------------------------------------------

# Root directory of package
_PACKAGE_ROOT = os.path.dirname(os.path.abspath(selenium_aem_nationals.__file__))
# Path to the log directory
_LOG_PATH = os.path.join(_PACKAGE_ROOT, 'log')


# Configurations
# ----------------------------------------------------------------

# General
# --------------------------------

# Implicit wait time for webdriver to poll DOM
IMPLICIT_WAIT = 10

# Browser Drivers
# --------------------------------

# Firefox webdriver initialization arguments
FIREFOX_KWARGS = {'log_path': os.path.join(_LOG_PATH, 'geckodriver.log')}

# Chrome webdriver initialization arguments
CHROME_KWARGS = {'service_log_path': os.path.join(_LOG_PATH, 'chromedriver.log')}

# Safari webdriver initialization arguments
SAFARI_KWARGS = {}

# Functions
# ----------------------------------------------------------------

def get_firefox_driver():
    """Returns webdriver.Firefox object using FIREFOX_KWARGS to initialize"""
    return webdriver.Firefox(**FIREFOX_KWARGS)

def get_chrome_driver():
    """Returns webdriver.Chrome object using CHROME_KWARGS to initialize"""
    return webdriver.Chrome(**CHROME_KWARGS)

def get_safari_driver():
    """Returns webdriver.Safari object using SAFARI_KWARGS to initialize"""
    return webdriver.Safari(**SAFARI_KWARGS)




