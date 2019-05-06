webdriver\_test\_tools.config.webdriver module
==============================================

.. automodule:: webdriver_test_tools.config.webdriver

   .. autoclass :: WebDriverConfig
      :members:
      :undoc-members:
      :exclude-members: LOG_PATH, SCREENSHOT_PATH

      .. attribute:: LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(webdriver_test_tools.__file__)), 'log')

         Path to the log directory. Defaults to the log subdirectory in the
         ``webdriver_test_tools`` package root directory

      .. attribute:: SCREENSHOT_PATH = os.path.join(os.path.dirname(os.path.abspath(webdriver_test_tools.__file__)), 'screenshot')

         Path to the screenshot directory. Defaults to the screenshot
         subdirectory in the ``webdriver_test_tools`` package root directory
        
