import requests
import logging
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/catalogue/category/books/music_14/index.html"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

logging.basicConfig(
    filename="scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

books = soup.find_all("article", class_="product_pod")

for book in books:
    title = book.h3.a["title"]
    price = book.find("p", class_="price_color").text

    logging.info(f"Title: {title}, Price: {price}")
    print(f"Title: {title}, Price: {price}")

books = soup.find_all("article", class_="product_pod")

logging.info(f"Status Code: {response.status_code}")
logging.info(f"Number of books found: {len(books)}")

print(f"Status Code: {response.status_code}")
print(f"Number of books found: {len(books)}")