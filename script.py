import re
from decimal import Decimal

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag


def detect_meat(product_name):
    product_name = product_name.lower()

    if 'stir fry' in product_name or 'seasoning' in product_name:
        return 'flavouring'

    if 'chicken' in product_name:
        return 'chicken'

    if ('pork' in product_name or 'bacon' in product_name):
        return 'pork'

    if ('beef' in product_name or 'rump' in product_name or 'steak' in product_name):
        return 'beef'

    print(f'Unknown meat: {product_name}')
    return 'unknown'


def convert_to_meat_type(product_list):
    """Convert a list of products into a combined list by meat."""

    meats = {}

    for grams, product_name in product_list:
        # What type of meat is this?
        meat = detect_meat(product_name)
        meats[meat] = meats.get(meat, 0) + grams

    return meats


def main():
    default_url = 'http://www.musclefood.com/march-great-tasting-meats'
    default_url = 'http://www.musclefood.com/bundles/variety-packs/simply-the-best-chicken-mince-selection.html'
    url = input('Please enter a URL: ') or default_url
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html5lib')

    # This the class used on the full screen / promo style hamper pages.
    product_names = soup.find_all(class_='prodhead-twoeight')

    # This is used on the full screen, two column style hamper page.
    if not product_names:
        product_names = soup.find_all(class_='prodhead-twoeight-lrg')

    if not product_names:
        # #product-options-wrapper h2
        wrapper = soup.find(id='product-options-wrapper')

        if wrapper:
            product_names = wrapper.find_all('h2')

    # Product detail page
    if not product_names:
        product_names = soup.find(id='productname')

    totals = []

    # Handle situations where we just get a single element/
    if isinstance(product_names, Tag):
        product_names = [product_names]

    for product in product_names:
        product_name = product.text.strip()

        # If the product name doesn't contain a gram value, disregard it.
        if not re.search(r'\d+k?g', product_name):
            print(f'Skipping {product_name} - no grams!')
            continue

        # Calculate the meat quantity.

        # First: 10 x 100g Item name
        first_format = re.match(r'^(\d+) ?x (\d+)g (.*)', product_name)

        if first_format:
            groups = first_format.groups()
            grams = Decimal(groups[0]) * Decimal(groups[1])

            totals.append((grams, groups[2]))
            continue

        # Second: 10-12 x 200g Item name (2.5kg)
        second_format = re.match(r'^\d+-\d+ ?x \d+g (.*) \(([\d\.]+)kg\)', product_name)

        if second_format:
            groups = second_format.groups()
            kgs = groups[1]
            grams = Decimal(kgs) * 1000

            totals.append((grams, groups[0]))
            continue

        # Third: 300g Mince
        third_format = re.match(r'^(\d+)g (.*)', product_name)

        if third_format:
            groups = third_format.groups()

            totals.append((Decimal(groups[0]), groups[1]))
            continue

        # Fourth: 1 x 2.5kg Item name
        fourth_format = re.match(r'^(\d+) ?x ([\d\.]+)kg (.*)', product_name)

        if fourth_format:
            groups = fourth_format.groups()
            kgs = groups[1]
            grams = Decimal(groups[0]) * Decimal(kgs) * 1000

            totals.append((grams, groups[2]))
            continue

        print(f'Not handled: {product_name}')

    # print('Totals:', totals)
    print(f'Meats: {convert_to_meat_type(totals)}')
if __name__ == '__main__':
    main()
