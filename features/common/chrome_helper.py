import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


TIMEOUT = 10


def get_element_by_xpath(driver, xpath, timeout=TIMEOUT):
    """
    Function to get element by xpath and return it if found
    :param driver: Chrome web driver
    :param xpath: element xpath
    :param timeout: time wait for driver to get object
    :return: element object
    """
    try:
        element = WebDriverWait(driver, timeout).until(ec.presence_of_element_located((By.XPATH, xpath)))
        return element
    except Exception as e:
        raise Exception(f"Couldn't get element, details: {e}")


def send_text(driver, xpath, text, timeout=TIMEOUT):
    """
    function to type text in Chrome edit texts
    :param driver:  Chrome web driver
    :param xpath: element xpath
    :param text: requested text
    :param timeout: time wait for driver to perform action
    :return: no return
    """
    element = get_element_by_xpath(driver, xpath, timeout)
    try:
        element.send_keys(text)
    except Exception as e:
        raise Exception(f"Couldn't send text, details: {e}")


def do_click(driver, xpath, timeout=TIMEOUT):
    """
    function to send click in Chrome browser
    :param driver: Chrome web driver
    :param xpath: element xpath
    :param timeout: time wait for driver to perform action
    :return: no return
    """
    element = get_element_by_xpath(driver, xpath, timeout)
    try:
        element.click()
        # sleep after click to visualize code execution in browser
        time.sleep(3)
    except Exception as e:
        raise Exception(f"Couldn't perform click, details: {e}")


def if_displayed(driver, xpath, timeout=TIMEOUT):
    """
    function to check if given element is displayed
    :param driver: Chrome web driver
    :param xpath: element xpath
    :param timeout: time wait for driver to perform action
    :return: returns boolean if object is displayed or not
    """
    element = get_element_by_xpath(driver, xpath, timeout)
    try:
        status = element.is_displayed()
        return status
    except Exception as e:
        raise Exception(f"Element is not displayed, details: {e}")


def validate_date_format(date_string):
    """
    function to validate date format before entering it to website
    :param date_string: day/month/year date format as string
    :return: returns false if string didn't match format otherwise return True and date values in list as string
    """
    parts = date_string.split('/')
    if len(parts) != 3:
        return False

    try:
        day = int(parts[0])
        month = int(parts[1])
        year = int(parts[2])
    except ValueError:
        return False

    if not (1 <= day <= 31):
        return False
    if not (1 <= month <= 12):
        return False
    if not (1900 <= year <= 2021):
        return False

    return True, [str(day), str(month), str(year)]
