"""Functions for scrolling elements into view"""


def into_view(driver, element, align_to_top=True):
    """Scroll to an element

    :param driver: Selenium WebDriver object
    :param element: WebElement to scroll to
    :param align_to_top: (Default = True) Aligns element to top of scrollable parent if True, aligns it to the bottom
        if False
    """
    script_string = 'arguments[0].scrollIntoView({});'.format(str(align_to_top).lower())
    driver.execute_script(script_string, element)

def to_and_click(driver, element, align_to_top=True):
    """Short hand function for scrolling an element into view and clicking it

    :param driver: Selenium WebDriver object
    :param element: WebElement to scroll to and click on
    :param align_to_top: (Default = True) Aligns element to top of scrollable parent if True, aligns it to the bottom if
        False
    """
    into_view(driver, element, align_to_top)
    element.click()

def to_position(driver, x, y):
    """Scroll window to the specified x,y coordinates

    Executes JavaScript window.scroll(x,y)

    :param driver: Selenium WebDriver object
    :param x: Horizontal scroll coordinate
    :param y: Vertical scroll coordinate
    """
    script_string = 'window.scroll({},{});'.format(x, y)
    driver.execute_script(script_string)

def to_element(driver, element, offset=0, align_to_top=True):
    """Vertically scroll to an element with an optional offset

    When align_to_top=True, the scroll y coordinate is calculated:
        element.offsetTop - offset
    When align_to_top=False, the scroll y coordinate is calculated:
        element.offsetTop + element.offsetHeight - window.innerHeight + offset

    :param driver: Selenium WebDriver object
    :param element: WebElement object for the target element
    :param offset: (Default = 0) Scroll offset
    :param align_to_top: (Default = True) Aligns element to the top of scrollable parent if True, aligns it to the
        bottom if False
    """
    scroll_y = int(element.get_property('offsetTop'))
    if align_to_top:
        scroll_y -= offset
    else:
        script_string = 'return window.innerHeight;'
        viewport_height = int(driver.execute_script(script_string))
        scroll_y += int(element.get_property('offsetHeight')) - viewport_height + offset
    to_position(driver, 0, scroll_y)

def into_view_fixed_nav(driver, target_element, fixed_element, additional_offset=0, align_to_top=True):
    """Scroll an element into view offset by the height of a fixed element so it's not obstructed

    :param driver: Selenium WebDriver object
    :param target_element: WebElement object for the target element
    :param fixed_element: WebElement object for the fixed nav
    :param additional_offset: (Default = 0) Additional offset from the top
    :param align_to_top: (Default = True) Aligns element to the top of scrollable parent if True, aligns it to the
        bottom if False
    """
    offset = int(fixed_element.get_property('offsetHeight')) + additional_offset
    to_element(driver, target_element, offset, align_to_top)


