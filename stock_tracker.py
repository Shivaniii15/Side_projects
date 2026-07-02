"""
A Python tool that fetches real-time stock prices for a predefined list of tickers, 
calculates profit/loss based on hardcoded buy prices, and exports the results into a clean csv report.
Developed by: Shivani 
"""

import logging
import yfinance as yf
import pandas as pd #handles data perfectly in tabular data. easy to export to excel.
from datetime import datetime
import os
import time



# -----------------------------
# CONFIG
# -----------------------------


logging.basicConfig(
    filename='stock_tracker.log',
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


#price is shown in usd because API return prices in native exchange currency of the stock. 

def load_portfolio(filename):
    portfolio = {}

    try:
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()

                if not line:
                    continue

                parts = line.split(",")

                if len(parts) != 2:
                    logging.warning(f"Invalid line: {line}")
                    continue

                symbol = parts[0].strip()
                try:
                    price = float(parts[1].strip())
                except ValueError:
                    logging.error(f"Invalid price for {symbol}")
                    continue

                portfolio[symbol] = price

    except FileNotFoundError:
        logging.error(f"File not found: {filename}")

    return portfolio

BUY_PRICES = load_portfolio(filename="stocks.txt")
STOCKS = list(BUY_PRICES.keys())

if not STOCKS:
    logging.error("No stocks loaded. Please check the stocks.txt file.")
    exit(1)

if not BUY_PRICES:
    logging.error("No buy prices loaded. Please check the stocks.txt file.")
    exit(1)



# -----------------------------
# FETCH PRICE 
# -----------------------------

def get_stock_price(symbol):

    """Fetch the current stock price using yfinance"""
    #connection to yahoo finance API.
    try:
        stock = yf.Ticker(symbol)

        history = stock.history(period="1d")

        #if data is not found, return 0 and logging.warning a message.
        if history.empty:
            logging.warning(f"No data found for {symbol}.")
            return 0
        
        """Get current price from the last trading day"""
        #history(period="1d") gets today's data, and "Close" gives the closing price. iloc[-1] gets the latest price.
        current_price = history["Close"].iloc[-1]
        return current_price
    
    except Exception as e:
        logging.error(f"Error fetching data for {symbol}: {e}")
        return 0


# -----------------------------
# CALCULATE P/L
# -----------------------------
def calculate_profit_loss(symbol, current_price):
    buy_price = BUY_PRICES.get(symbol, 0)
    pnl = current_price - buy_price
    return pnl


# -----------------------------
# MAIN LOGIC
# -----------------------------

data = []

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

for stock in STOCKS:

    current_price = get_stock_price(stock)

    if current_price == 0:
        logging.warning(f"Skipping {stock} due to missing data.")
        continue

    buy_price = BUY_PRICES[stock]

    pnl = current_price - buy_price

    data.append({
        "Timestamp": timestamp,
        "Stock": stock,
        "Buy Price": round(buy_price, 2),
        "Current Price": round(current_price, 2),
        "P/L": round(pnl, 2)
    })

#-----------------------------
# EXPORT TO CSV
#-----------------------------

df = pd.DataFrame(data)

#one clean row per stock per run
data_file = "stock_data.csv"
data_exists = os.path.isfile(data_file)
df.to_csv(data_file, index=False, mode='a', header=not data_exists)

#one row per run, total pnl only
total_pnl = sum(item["P/L"] for item in data)
summary_file = "stock_summary.csv"
summary_exists = os.path.isfile(summary_file)

summary_df = pd.DataFrame([{
    "Timestamp": timestamp,
    "Total P/L": round(total_pnl, 2)
}])

summary_df.to_csv(summary_file, index=False, mode='a', header=not summary_exists)
print(f"Summary saved to: {os.path.abspath(summary_file)}")


def main():
    print("Stock Tracker Report Generated: stock_data.csv and stock_summary.csv")
    logging.info("CSV report generated: stock_data.csv and stock_summary.csv\n")

if __name__ == "__main__":
    while True:
        main()
        logging.info("Waiting 10 seconds before next run...")
        time.sleep(10)