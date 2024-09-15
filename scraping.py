import requests
from bs4 import BeautifulSoup
import pandas as pd

# Step 1: Scrape Competitor Prices
def scrape_competitor_prices(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Assuming the price is inside a tag with class "product-price"
    price_tag = soup.find('span', class_='product-price')
    
    # Convert to a float if price is found
    price = float(price_tag.text.replace('$', '').replace(',', '')) if price_tag else None
    return price

# Step 2: Analyze Prices
def adjust_price(my_price, competitor_price):
    if competitor_price and my_price > competitor_price:
        # Reduce your price by 5% if competitor's price is lower
        return round(competitor_price * 0.95, 2)
    return my_price

# Step 3: Update Your Product Price on Your Platform
def update_product_price(product_id, new_price):
    API_URL = f"https://api.your-ecommerce-platform.com/products/{product_id}/price"
    API_TOKEN = "your_api_token"
    
    headers = {'Authorization': f'Bearer {API_TOKEN}', 'Content-Type': 'application/json'}
    payload = {'price': new_price}
    
    response = requests.put(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        print(f"Price for product {product_id} updated successfully to {new_price}.")
    else:
        print(f"Failed to update price for product {product_id}: {response.text}")

# Main Flow: Price Monitoring and Adjustment
def monitor_and_adjust():
    # Example product data (in real use-case, this will be dynamic)
    products = [{'id': 1, 'my_price': 100.00, 'competitor_url': 'https://competitor.com/product1'}]
    
    for product in products:
        competitor_price = scrape_competitor_prices(product['competitor_url'])
        new_price = adjust_price(product['my_price'], competitor_price)
        update_product_price(product['id'], new_price)

# Start monitoring and adjusting
monitor_and_adjust()
