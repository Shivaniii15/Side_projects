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


row = {
    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

total_pnl = 0

for stock in STOCKS:
    current_price = get_stock_price(stock)

    if current_price == 0:
        logging.info(f"Skipping {stock} due to missing data.")
        continue

    buy_price = BUY_PRICES[stock]

    pnl = calculate_profit_loss(stock, current_price)

    total_pnl += pnl
    
    row[f"{stock}_Buy"] = round(buy_price, 2)
    row[f"{stock}_Current"] = round(current_price, 2)
    row[f"{stock}_P/L"] = round(pnl, 2)

row ["Total P/L"] = round(total_pnl, 2)

#-----------------------------
# EXPORT TO CSV
#-----------------------------


df = pd.DataFrame([row], index=[0])

#checks if the file already exists
file_exists = os.path.isfile("new_stock_tracker.csv")

#append data
df.to_csv("new_stock_tracker.csv", index=False, mode='a', header=not file_exists)


def main():
    print("Stock Tracker Report Generated: new_stock_tracker.csv")
    logging.info("CSV report generated: new_stock_tracker.csv\n")

if __name__ == "__main__":
    main()