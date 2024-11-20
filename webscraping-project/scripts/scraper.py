import requests
import pandas as pd
import re
import os
import math
from bs4 import BeautifulSoup

# Constants 
BASE_URL = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=monitor&_sacat=0&LH_ItemCondition=1000&LH_FS=1&rt=nc&LH_All=1'
ITEMS_PER_PAGE = 60

def get_total_items(soup):
    # Returns the total number of items found.
    count_element = soup.find('div', class_='srp-controls__control srp-controls__count')
    total_text = count_element.get_text().strip()
    
    # the regular expression [\d.]+ so look numbers and dots in text
    number = re.search(r'[\d.]+', total_text).group().replace('.', '') # Extract numbers from text (e.g., converts "1.234 results" to "1234")
    return int(number)

def clean_price(price_text):
    # Cleans and formats the price text to a float number.
    if 'a' in price_text:
        price_text = price_text.split(' a ')[0]
    
    return float(price_text.replace('\xa0', '')
                          .replace('&nbsp;', '')
                          .replace(' ', '')
                          .replace('R$', '')
                          .replace(',', '.'))

def scrape_product(product):
    # Extracts title and price from a product.
    title_element = product.find('div', class_='s-item__title')
    price_element = product.find('span', class_='s-item__price')
    
    if not title_element or not price_element or 'Shop on eBay' in title_element.get_text():
        return None
    
    return {
        'title': title_element.get_text().strip(),
        'price': clean_price(price_element.get_text().strip())
    }

def main():
    # path to save the datas
    path = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(path, '..', 'data')
    
    # Make first request to get total pages
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    total_items = get_total_items(soup)
    total_pages = math.ceil(total_items / ITEMS_PER_PAGE)
    
    # Collect data
    products_data = {'brand': [], 'price': []}
    
    for page in range(1, total_pages + 1):
        url_pag = f"{BASE_URL}&_pgn={page}"
        response = requests.get(url_pag)
        soup = BeautifulSoup(response.content, 'html.parser')
        products = soup.find_all('div', class_='s-item__info clearfix')
        print(url_pag)
        
        for product in products:
            product_data = scrape_product(product)
            if product_data:
                products_data['brand'].append(product_data['title'])
                products_data['price'].append(product_data['price'])
    
    # save data
    df = pd.DataFrame(products_data)
    df.to_csv(os.path.join(data_dir, 'CSVs_Files/monitor.csv'), encoding='utf8', index=False)

if __name__ == '__main__':
    main()