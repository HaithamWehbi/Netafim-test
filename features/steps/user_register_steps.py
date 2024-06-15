from selenium.webdriver.support.ui import Select
from behave import *
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options
from features.common.chrome_helper import get_element_by_xpath, validate_date_format, if_displayed, do_click, send_text
from features.common.details_storage import locators, countries


@given('launch the browser')
def step_impl(context):
    options = Options()
    # add 'u block' extension to prevent handling website ads
    options.add_extension(r"C:\chrome_ext\uB.crx")
    context.driver = webdriver.Chrome(options=options)


@when('I navigate to website homepage "{url}"')
def step_impl(context, url):
    # open website
    context.driver.get(url)


@then('verify that homepage is displayed')
def step_impl(context):
    # check if website launched by checking image visibility
    status = if_displayed(context.driver, locators['home_page_image'])
    assert status is True


@when('clicking on sign up button')
def step_impl(context):
    # go to sign up / login page
    do_click(context.driver, locators['sign_up_icon'])


@then('verify New User sign is displayed')
def step_impl(context):
    status = if_displayed(context.driver, locators['new_user_sign'])
    assert status is True


@when('entering a name and email "{name}" "{email}"')
def step_impl(context, name, email):
    send_text(context.driver, locators['sign_up_name'], name)
    send_text(context.driver, locators['sign_up_email'], email)


@when('click signup button')
def step_impl(context):
    # sign up with name and email
    do_click(context.driver, locators['sign_up_button'])


@then('verify that Enter Account Info is displayed')
def step_impl(context):
    status = if_displayed(context.driver, locators['acc_info_text'])
    assert status is True


@when('filling details: "{title}", "{name}", "{password}", "{date_of_birth}"')
def step_impl(context, title, name, password, date_of_birth):
    # check title if matches website options
    if title == 'mr':
        do_click(context.driver, locators['mr_radio'])
    elif title == 'mrs':
        do_click(context.driver, locators['mrs_radio'])
    else:
        raise Exception("choose title as mr or mrs.")

    # fill name and password
    send_text(context.driver, locators['name_field'], name)
    send_text(context.driver, locators['password_field'], password)

    # get date selectors elements
    day_list = get_element_by_xpath(context.driver, locators['day_list'])
    month_list = get_element_by_xpath(context.driver, locators['month_list'])
    year_list = get_element_by_xpath(context.driver, locators['year_list'])

    # check if given date matches date format
    status, date_list = validate_date_format(date_of_birth)
    if status:
        # get selectors object and select by value
        try:
            day_selection = Select(day_list)
            day_selection.select_by_value(date_list[0])
            month_selection = Select(month_list)
            month_selection.select_by_value(date_list[1])
            year_selection = Select(year_list)
            year_selection.select_by_value(date_list[2])
        except Exception as e:
            raise Exception(f"Couldn't select date, details: {e}")
    else:
        raise Exception("date format should be day/month/year. example: 13/07/2020")


@when('select sign up checkbox')
def step_impl(context):
    news_checkbox = get_element_by_xpath(context.driver, locators['news_checkbox'])
    try:
        # scroll to news checkbox then select checkbox
        context.driver.execute_script("arguments[0].scrollIntoView(true);", news_checkbox)
        WebDriverWait(context.driver, 10).until(ec.visibility_of(news_checkbox))
        news_checkbox.click()
    except Exception as e:
        raise Exception(f"something went wrong, details: {e}")


@when('select receive offers')
def step_impl(context):
    do_click(context.driver, locators['offers_checkbox'])


@when('filling more details: "{last_name}", "{first_name}", "{company}", "{address}", "{address2}", "{country}", '
      '"{state}", "{city}", "{zipcode}", "{number}"')
def step_impl(context, last_name, first_name, company, address, address2, country, state, city, zipcode, number):
    # fill details
    send_text(context.driver, locators['first_name_field'], first_name)
    send_text(context.driver, locators['last_name_field'], last_name)
    send_text(context.driver, locators['company_field'], company)
    send_text(context.driver, locators['address_field'], address)
    send_text(context.driver, locators['address2_field'], address2)

    country_list = get_element_by_xpath(context.driver, locators['country_list'])
    try:
        country_selection = Select(country_list)
        # check if given country not found in website options
        if country not in countries:
            raise Exception(f"Error: available countries: {countries}")
        # select country by value
        country_selection.select_by_value(country)
    except Exception as e:
        raise Exception(f"Couldn't select element, details: {e}")

    # fill details
    send_text(context.driver, locators['state_field'], state)
    send_text(context.driver, locators['city_field'], city)
    send_text(context.driver, locators['zipcode_field'], zipcode)
    send_text(context.driver, locators['mobile_number_field'], number)


@when('clicking on create account button')
def step_impl(context):
    scroll_element = get_element_by_xpath(context.driver, locators['mobile_number_field'])
    try:
        # scroll down to one element before the create button to prevent issues since it's last in page
        context.driver.execute_script("arguments[0].scrollIntoView(true);", scroll_element)
        WebDriverWait(context.driver, 10).until(ec.visibility_of(scroll_element))
    except Exception as e:
        raise Exception(f"something went wrong, details: {e}")

    # click button to create account
    do_click(context.driver, locators['create_button'])


@then('verify that Account Created is visible')
def step_impl(context):
    status = if_displayed(context.driver, locators['acc_created_text'])
    assert status is True


@when('click on continue button')
def step_impl(context):
    do_click(context.driver, locators['continue_after_create'])


@then('verify that Logged In As Username is visible')
def step_impl(context):
    status = if_displayed(context.driver, locators['logged_in_icon'])
    assert status is True


@when('click delete account button')
def step_impl(context):
    do_click(context.driver, locators['delete_icon'])


@then('verify Account Deleted is visible and click Continue button')
def step_impl(context):
    # check if account deleted and click continue
    status = if_displayed(context.driver, locators['acc_deleted_text'])
    do_click(context.driver, locators['continue_after_delete'])
    assert status is True


def after_all(context):
    context.driver.quit()
