import requests
import logging

logging.basicConfig(
    filename="scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

url = "https://books.toscrape.com/catalogue/category/books/music_14/index.html"

response = requests.get(url)
logging.info(f"Status Code: {response.status_code}")
logging.info(f"Response Text (first 500 chars): {response.text[:500]}")

print(response.status_code)
print(response.text[:500])