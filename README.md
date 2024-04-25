# BOMIA LAPTOP STORE

This project is a basic shopping website that sells laptops. The laptops dataset was gotten from [Kaggle](https://www.kaggle.com/datasets?search=E-commerce+)

## SETTING UP THE APPLICATION
How to start it
----------------
1. Create a new project folder called ‘solo’ and then cd into the folder via the terminal and execute these commands:
   ```
   mkdir solo
   cd solo
    ```
### CREATING THE ENVIRONMENT
2. To set up the application run the following commands:

    ```
    pyenv local 3.10.7 # this sets the local version of python to 3.10.7
    python3 -m venv .venv # this creates the virtual environment for you
    source .venv/bin/activate # this activates the virtual environment
    pip install --upgrade pip # this installs pip, and upgrades it if required.
	pip install faker # installs faker
    ```

3. We used Django (https://www.djangoproject.com) as our web framework for the application. Install Django with:
    ```
    pip install Django==4.1.2
    ```

4. Create the site using the django admin tools:
    ```
    django-admin startproject ecom .
    ```

5. Specify settings for the site in ecom/settings.py:
    - Add `import os` above the line for pathlib import Path.
    - Add `STATIC_ROOT = os.path.join(BASE_DIR, 'static')` at the end of the file.
    - Modify `ALLOWED_HOSTS` to include appropriate hosts.

6. Start the development server:
    ```
    python3 manage.py runserver
    ```
    •	If you’re doing this on another platform, then you might need to use this instead (change the port number from 8000 as required):

    ```
    python3 manage.py runserver 0.0.0.0:8000
    ```

Creating the Story content
---------------------------
1. Leave the server running and open a new terminal.
2. Navigate to the project directory and create a new app:
    ```
    python3 manage.py startapp shop
    ```

3. Modify ecom/urls.py to include the urls for the 'shop' app.
4. Add 'shop' to the INSTALLED_APPS in ecom/settings.py.
5. Create urls.py in the 'shop' folder with appropriate URL mappings.

### SETTING UP THE DATABASE
The database used is SQLite3.
---------------------------
1. Configure the database:
    ```
    python3 manage.py migrate
    ```
2. After initializing the database, run these commands to create the tables in the database:
	```
	python3 manage.py makemigrations
	python3 manage.py migrate
	```

3. Populating the database
The app uses Faker to generate random customers and orders and the products are parsed from the .csv file in 'shop/dataset/laptops.csv' using the parameters specified in '/management/commands/parse_csv.py'. The dataset was reduced due to cloud database limitations and very long time to build application. You populate the data using the command:
	```
	python3 manage.py parse_csv
	```

4.  Creating admin
You can create an admin user to monitor the customers and orders made in the shop. There is also a dashboard that monitors the sales made by the customers. You can also add more admins or customers. Run this command:
	```
	python3 manage.py createsuperuser
	```

5. Running the server

	```
	python3 manage.py runserver # on local machine
	python3 manage.py runserver 0.0.0.0:8000 # to run on codio
	````

6. Visit the following URL in your Web browser to view the application:
    ```
    https://rainbowlesson-aztecamadeus-8000.codio-box.uk/
    ```

7. Visit the following URL in your Web browser to view the admin:
     ```
    https://rainbowlesson-aztecamadeus-8000.codio-box.uk/admin
    ```
Templates
---------
- For the templates, we create the necessary HTML folders(admin, cart, customer, orders, registration, shop) and files (base.html, nav, pagination.html) in the 'shop/templates' directory.

Methodology
-----------
- Behave tests was used to implement Behavior Driven Development using other tools such as selenium and the chrome driver. It ensures reliability and adaptability of the codebase.

# Maintenance
GitHub was used for version control and code maintenance.

# Testing
Create features folder. Download chrome driver. Create features file. Sample code below.
Create product.feature:

  ```python
    Feature: search products

    Scenario: checkout a product
        Given we search a product
        When we enter the query
        Then it succeeds

Create checkout.py in steps folder		
import urllib
from urllib.parse import urljoin
from behave import given, when, then
from selenium.webdriver.common.by import By

@given(u'we search a product')
def user_on_product_newpage(context):
	base_url = urllib.request.url2pathname(context.test_case.live_server_url)
	print(base_url)
	open_url = urljoin(base_url,'/search/')
	context.browser.get(open_url)


@when(u'we enter the query')
def user_enters_the_query(context):
	print(context.browser.page_source)
	name_textfield = context.browser.find_element('name', 'query')
	name_textfield.send_keys('K')
	search_button = context.browser.find_element(By.CSS_SELECTOR,'input[type="submit"]')
	search_button.click()


# @then(u'it succeeds')
# def step_impl(context):
# # 	base_url = urllib.request.url2pathname(context.test_case.live_server_url)
# # 	open_url = urljoin(base_url,"/search/?query=K")
# # 	context.browser.get(open_url)
# # 	print(context.browser.page_source)
# # 	# expected_product = 'Kepler'
# # 	# id_query = context.browser.find_element(By.NAME,'id_query')
# # 	# assert expected_product in id_query.text
# # 	assert 'Kepler' in context.browser.page_source
@then(u'it succeeds')
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


  ```
run behave command in terminal to do testing.

# USAGE
1. Browse Laptops: Navigate to the homepage to view the list of available laptops.
2. View Details: Click on a laptop to view detailed information, specifications, and pricing.
3. Add to Cart: Click the "Add to Cart" button to add a laptop to your shopping cart.
4. Adjust Cart: In the shopping cart, adjust the quantity of laptops or remove items as needed.
5. Checkout: Proceed to checkout to complete your purchase.