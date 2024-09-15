import pandas as pd
import requests
import os

API_URL = "https://api.your-ecommerce-platform.com/products"
API_TOKEN = "your_api_token"

# Function to upload a product to the platform
def upload_product(product):
    headers = {'Authorization': f'Bearer {API_TOKEN}', 'Content-Type': 'application/json'}
    response = requests.post(API_URL, headers=headers, json=product)
    if response.status_code == 201:
        print(f"Product {product['name']} uploaded successfully.")
    else:
        print(f"Error uploading product {product['name']}: {response.text}")

# Function to upload image files and return their URL
def upload_image(image_path):
    if os.path.exists(image_path):
        files = {'file': open(image_path, 'rb')}
        response = requests.post(f"{API_URL}/upload_image", files=files, headers={'Authorization': f'Bearer {API_TOKEN}'})
        if response.status_code == 200:
            return response.json().get('url')
    return None

# Main function to process product data from CSV and perform bulk upload
def bulk_upload(csv_file):
    data = pd.read_csv(csv_file)
    for _, row in data.iterrows():
        image_url = upload_image(row['image_path'])
        product = {'name': row['product_name'], 'description': row['description'], 'price': row['price'], 'image_url': image_url}
        upload_product(product)

# Script execution begins here
if __name__ == "__main__":
    bulk_upload('products.csv')
