# Book Price Scraper

A learning project: scrapes book listings from [books.toscrape.com](https://books.toscrape.com) (Music category) and tracks prices over time in a SQLite database.

## What it does

1. Fetches the Music category page using `requests`
2. Parses out each book's title, URL, and price using `BeautifulSoup`
3. Saves data to a local SQLite database (`books.db`):
   - New books are added once
   - Every run adds a new price snapshot, so prices can be tracked over time
4. Logs each run's activity to `scraper.log`

## Why books.toscrape.com

Real e-commerce sites (eBay, Etsy, Newegg, Target, Barnes & Noble) were checked first via `robots.txt` — most disallow scraping their search pages, and several load prices via JavaScript (requiring heavier tools like Selenium). `books.toscrape.com` is a sandbox site built specifically for practicing scraping, with static HTML and explicit permission to scrape — better suited for learning the core pipeline before tackling a harder real-world target.

## Database schema

**`books`** — one row per unique book (identified by URL, since titles can repeat)
| column | type |
|---|---|
| id | INTEGER PRIMARY KEY |
| title | TEXT |
| url | TEXT UNIQUE |

**`price_history`** — one new row every scrape run, linked to `books`
| column | type |
|---|---|
| id | INTEGER PRIMARY KEY |
| book_id | INTEGER (foreign key → books.id) |
| price | REAL |
| scraped_at | DATETIME |

This two-table design (entity table + time-stamped event table) is what makes tracking price changes over time possible without duplicating book info on every run.

## Setup

```
pip install requests beautifulsoup4
```

## Running it

```
python scraper.py
```

Each run:
- Adds any new books found to the `books` table
- Adds a fresh price entry to `price_history` for every book found (even if the price hasn't changed)

View the database using [DB Browser for SQLite](https://sqlitebrowser.org).

## Progress log

- [x] Fetch page with `requests` + error handling
- [x] Parse listings with `BeautifulSoup`
- [x] Design two-table schema (books + price_history)
- [x] Insert-or-get logic to avoid duplicate books across runs
- [x] Basic logging to `scraper.log`
- [ ] Expand logging to cover every pipeline stage (fetch, parse, DB connect, commit)
- [ ] Scheduling (cron / Task Scheduler) to run automatically over time
- [ ] Query/visualize price history once enough data has accumulated

## Notes

- Prices on this site are randomly assigned dummy data — useful for learning the pipeline, not real price tracking. The same script structure can point at a real, scraper-friendly store later with minimal changes (mainly the selectors in the parsing step).