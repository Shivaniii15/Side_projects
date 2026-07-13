# side-quests

A collection of small, self-directed Python projects — built to learn practical, real-world skills one problem at a time: web scraping, file-system automation, data persistence, and reporting.

Each project is self-contained in its own folder, with its own README covering setup and usage in detail. This file is just a map.

## Projects

### 📚 [book-scraper](./book-scraper)
Scrapes book listings and prices, storing them in a SQLite database designed to track price changes over time (rather than just a single snapshot).
`Python` · `requests` · `BeautifulSoup` · `SQLite`

### 📈 [stock-tracker](./stock-tracker)
Fetches live stock prices for a configurable portfolio, calculates profit/loss against buy prices, and exports a formatted Excel report.
`Python` · `yfinance` · `pandas` · `openpyxl`

### 🗂️ [file-monitor](./file-monitor)
Watches a folder for new files, automatically renames and organizes them, logs every action to a database, and sends desktop notifications — with a Streamlit dashboard to visualize activity.
`Python` · `watchdog` · `SQLite` · `Streamlit`

## Why these projects

Each one was picked to deliberately practice a different practical skill: pulling data from the outside world (scraping, APIs), storing and modeling it correctly (SQL schema design, tracking change over time), automating a repetitive real task (file organization), and presenting results clearly (Excel reports, live dashboards). Together they cover a good chunk of what a working data/automation pipeline actually involves, end to end.

## Getting started

Each project folder has its own `README.md` with specific setup and usage instructions — start there.
