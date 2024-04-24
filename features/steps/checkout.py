import urllib
from urllib.parse import urljoin
from behave import given, when, then
from selenium.webdriver.common.by import By

@given(u'we search a product')
def user_on_product_newpage(context):
    base_url = context.config.server_url
    print(base_url)
    open_url = urljoin(base_url, '/search/')
    context.browser.get(open_url)


@when(u'we enter the query')
def user_enters_the_query(context):
    print(context.browser.page_source)
    name_textfield = context.browser.find_element(By.NAME, 'query')
    name_textfield.send_keys('K')
    search_button = context.browser.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
    search_button.click()


@then(u'it succeeds i want')
def step_impl(context):
    # Search for the product
    search_box = context.browser.find_element(By.NAME, 'query')
    search_box.send_keys('Kepler')
    search_box.submit()

    # Click on the link of the first search result
    search_results = context.browser.find_elements(By.CSS_SELECTOR, '.product-list-item a')
    assert len(search_results) > 0, 'No search results found'
    first_result = search_results[0]
    detail_url = first_result.get_attribute('href')
    context.browser.get(detail_url)

    # Check that we are on the product detail page
    assert 'Kepler' in context.browser.page_source
