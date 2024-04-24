import csv
from decimal import Decimal
from django.core.management.base import BaseCommand
from shop.models import Product, Category
import uuid

class Command(BaseCommand):
    help = 'Load data from csv'

    def handle(self, *args, **options):
        # Drop the data from the table so that if we rerun the file, we don't repeat values
        Category.objects.all().delete()
        Product.objects.all().delete()
        print("Tables dropped successfully")
        # Create categories and assign products
        file_path = 'shop/dataset/laptops.csv'
        parsed_data = parse_csv_file(file_path)
        create_categories_from_csv(parsed_data)
        assign_products_to_categories(parsed_data)


def parse_csv_file(file_path):
    parsed_data = []
    with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        next(reader)  # skip the header line
        for row_number, row in enumerate(reader, start=1):
            brand = row.get('Brand', '').strip()  # Remove leading/trailing whitespace
            print(f"Processing row {row_number}:")
            print(f"   Brand: '{brand}'")
            parsed_row = {
                'brand': brand,
                'product_name': row.get('Model', ''),
                'picture_url': row.get('picture', ''),
                'price_in_gbp': row.get('Price', ''),
            }
            parsed_data.append(parsed_row)
    return parsed_data

from django.utils.text import slugify

def create_categories_from_csv(parsed_data):
    for item in parsed_data:
        brand = item['brand']
        if brand:
            category_name = brand.strip()
            slug = slugify(category_name)  # Generate slug from category name
            while Category.objects.filter(slug=slug).exists():  # Check for existing slug
                # Slug exists, generate a new unique slug
                slug = slugify(category_name) + '-' + str(uuid.uuid4())[:8]
            category, created = Category.objects.get_or_create(name=category_name, defaults={'slug': slug})
            if created:
                print(f"Created category: {category_name}")
        else:
            print("Warning: Missing brand for a row.")


def preprocess_price(price_str):
    # Convert the price string to a decimal number
    try:
        # Remove commas and other characters that are not part of the number
        price_str = price_str.replace(',', '').replace('£', '').replace('$', '')
        return Decimal(price_str)  # Assuming prices are in GBP or another compatible format
    except Exception as e:
        # Handle any errors during price preprocessing
        print(f"Error preprocessing price: {e}")
        return None  # Return None if preprocessing fails


from django.utils.text import slugify

def assign_products_to_categories(parsed_data):
    empty_brand_count = 0  # Initialize count for empty 'Brand' column
    # Assign each product to its corresponding category based on the 'Brand' column
    for item in parsed_data:
        try:
            brand = item['brand']
            if brand:  # Check if brand is not empty or missing
                brand = brand.strip()  # Remove leading/trailing whitespace
                product_name = item['product_name']
                price_str = item['price_in_gbp']
                price = preprocess_price(price_str)
                image_url = item['picture_url']
                # Get or create the category for the brand
                category, _ = Category.objects.get_or_create(name=brand)
                # Create the product only if price is successfully processed
                if price is not None:
                    # Generate a slug for the product
                    slug = slugify(product_name)[:50]  # Limit slug length to 50 characters
                    # Check if a product with the same slug and category already exists
                    if not Product.objects.filter(slug=slug, category=category).exists():
                        Product.objects.create(
                            name=product_name,
                            price=price,
                            description='',
                            image=image_url,
                            category=category,
                            slug=slug  # Assign the generated slug to the product
                        )
                    else:
                        print(f"Product '{product_name}' with category '{category.name}' already exists.")
            else:
                empty_brand_count += 1  # Increment count for empty 'Brand' column
        except Exception as e:
            print(f"Error creating product: {e}")
    # Print a summary message for empty 'Brand' column
    if empty_brand_count:
        print(f"Warning: 'Brand' column is empty or missing for {empty_brand_count} row(s).")
