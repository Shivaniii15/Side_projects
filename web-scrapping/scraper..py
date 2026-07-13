import requests
import logging
from bs4 import BeautifulSoup
import sqlite3

logging.basicConfig(
    filename="scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

url = "https://books.toscrape.com/catalogue/category/books/music_14/index.html"

try:
    response = requests.get(url)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    logging.error(f"Request failed: {e}")
    print(f"Request failed: {e}")
    exit()

soup = BeautifulSoup(response.text, "html.parser")

# Connect to SQLite database
conn = sqlite3.connect("books.db")
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        url TEXT UNIQUE
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS price_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER,
        price REAL,
        scraped_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (book_id) REFERENCES books (id)
    )
""")

books = soup.find_all("article", class_="product_pod")

# Insert book data into the database
for book in books:
    try:
        title = book.h3.a["title"]
        relative_url = book.h3.a["href"]
        price_text = book.find("p", class_="price_color").text
        price = float(price_text.replace("£", "").replace("Â", ""))

        cursor.execute("SELECT id FROM books WHERE url = ?", (relative_url,))
        existing = cursor.fetchone()

        if existing:

            #is book is already there, just reuse its existing id
            book_id = existing[0]
            cursor.execute("INSERT INTO price_history (book_id, price) VALUES (?, ?)", (book_id, price))
        else:
            #new book, insert it and get its id
            cursor.execute("INSERT INTO books (title, url) VALUES (?, ?)", (title, relative_url))
            book_id = cursor.lastrowid
            logging.info(f"New book inserted: {title}")
            cursor.execute("INSERT INTO price_history (book_id, price) VALUES (?, ?)", (book_id, price))

    except (AttributeError, ValueError) as e:
        logging.warning(f"Failed to insert book into database: {e}")
        
conn.commit()

cursor.execute("SELECT name FROM sqlite_master WHERE type ='table'")
print(cursor.fetchall())

conn.close()


logging.info(f"Status Code: {response.status_code}")
logging.info(f"Number of books found: {len(books)}")

print(f"Status Code: {response.status_code}")
print(f"Number of books found: {len(books)}")
