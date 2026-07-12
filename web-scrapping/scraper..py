import requests
import logging
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/catalogue/category/books/music_14/index.html"

try:
    response = requests.get(url)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    logging.error(f"Request failed: {e}")
    print(f"Request failed: {e}")
    exit()

soup = BeautifulSoup(response.text, "html.parser")

logging.basicConfig(
    filename="scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

books = soup.find_all("article", class_="product_pod")

for book in books:
    title = book.h3.a["title"]
    price_text = book.find("p", class_="price_color").text
    price = float(price_text.replace("£", "").replace("Â", ""))

    logging.info(f"Title: {title}, Price: {price}")
    print(f"Title: {title}, Price: {price}")


logging.info(f"Status Code: {response.status_code}")
logging.info(f"Number of books found: {len(books)}")

print(f"Status Code: {response.status_code}")
print(f"Number of books found: {len(books)}")