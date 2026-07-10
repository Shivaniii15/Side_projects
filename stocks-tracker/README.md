# stocks-tracker

# Stock Price Tracker & P/L Reporter

A Python tool that fetches real-time stock prices for a predefined list of tickers, calculates profit/loss based on hardcoded buy prices, and exports the results into a clean Excel report.

---

## Features

- Fetches live stock prices using the [yfinance](https://pypi.org/project/yfinance/) library (powered by Yahoo Finance)
- Calculates **Profit/Loss (P/L)** per stock based on a configured buy price
- Exports results to a formatted **Excel spreadsheet** (`stock_tracker.xlsx`)
- Supports any list of stock tickers (e.g. `AAPL`, `TSLA`, `MSFT`)

---

## Tech Stack

- **Language:** Python 3
- **Libraries:**
  - [`yfinance`](https://pypi.org/project/yfinance/) — fetches stock data from Yahoo Finance
  - [`pandas`](https://pypi.org/project/pandas/) — handles tabular data and Excel export
  - [`openpyxl`](https://pypi.org/project/openpyxl/) — required by pandas for `.xlsx` output

---

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/stock-tracker.git
   cd stock-tracker
   ```

2. **Install dependencies**
   ```bash
   pip install yfinance pandas openpyxl
   ```

---

## Usage

Run the script directly:

```bash
python stock_tracker.py
```

This will generate a `stock_tracker.xlsx` file in the current directory with the following columns:

| Stock | Buy Price | Current Price | P/L |
|-------|-----------|---------------|-----|
| AAPL  | 100.0     | ...           | ... |
| TSLA  | 700.0     | ...           | ... |

> Prices are returned in the **native exchange currency** of each stock (typically USD for US-listed tickers).

---

## Configuration

Edit the following variables at the top of `stock_tracker.py` to customise your portfolio:

```python
# List of stock tickers to track
STOCKS = ["AAPL", "GOOGL", "TSLA", "AMZN", "MSFT", "NKE", "META"]

# Your buy price per ticker (in USD)
BUY_PRICES = {
    "AAPL": 100.0,
    "GOOGL": 3000.0,
    "TSLA": 700.0,
    ...
}
```

---

## Output

The script overwrites `stock_tracker.xlsx` on each run. Make sure to rename or back up the file if you want to preserve a previous report.

---

## License

This project is open source and available under the [MIT License](LICENSE).