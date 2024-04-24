import os
import django
from behave import fixture, use_fixture
from django.test.runner import DiscoverRunner
from django.test.testcases import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Set up Django environment
os.environ["DJANGO_SETTINGS_MODULE"] = "ecom.settings"
django.setup()

# Set up ChromeOptions
chrome_options = Options()
chrome_options.add_argument('--no-proxy-server')
chrome_options.add_argument("--proxy-server='direct://'")
chrome_options.add_argument("--proxy-bypass-list=*")

# Fixture to set up Django test runner
@fixture
def django_test_runner(context):
    context.test_runner = DiscoverRunner()
    context.test_runner.setup_test_environment()
    context.old_db_config = context.test_runner.setup_databases()
    yield
    context.test_runner.teardown_databases(context.old_db_config)
    context.test_runner.teardown_test_environment()

# Fixture to set up Django test case
@fixture
def django_test_case(context):
    context.test_case = LiveServerTestCase
    context.test_case.setUpClass()
    yield
    context.test_case.tearDownClass()
    del context.test_case

# Before all scenarios: Set up Django test runner and Selenium WebDriver
def before_all(context):
    use_fixture(django_test_runner, context)
    browser = webdriver.Chrome(options=chrome_options)
    browser.set_page_load_timeout(20)  # Adjust timeout as needed
    context.browser = browser

# Before each scenario: Set up Django test case
def before_scenario(context, scenario):
    use_fixture(django_test_case, context)

# After all scenarios: Quit Selenium WebDriver
def after_all(context):
    if hasattr(context, 'browser'):
        context.browser.quit()
