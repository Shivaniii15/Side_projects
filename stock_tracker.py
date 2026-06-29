"""
A Python tool that fetches real-time stock prices for a predefined list of tickers, 
calculates profit/loss based on hardcoded buy prices, and exports the results into a clean csv report.
Developed by: Shivani 
"""

import logging
import yfinance as yf
import pandas as pd #handles data perfectly in tabular data. easy to export to excel.


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

#store data in a list
data = []

for stock in STOCKS:
    current_price = get_stock_price(stock)

    if current_price == 0:
        logging.info(f"Skipping {stock} due to missing data.")
        continue

    pnl = calculate_profit_loss(stock, current_price)

    data.append({
        "Stock": stock,
        "Buy Price": BUY_PRICES.get(stock, 0),
        "Current Price": round(current_price, 2),
        "P/L": round(pnl, 2)
})

df = pd.DataFrame(data)
total_pnl = df["P/L"].sum()
df.loc[len(df.index)] = ["Total", None, None, round(total_pnl, 2)]  # Add a total row at the end

#make the csv file and save it to the current directory.
#overwrites existing one
df.to_csv("stock_tracker.csv", index=False)


def main():
    print("Stock Tracker Report Generated: stock_tracker.csv")
    logging.info("CSV report generated: stock_tracker.csv\n")

if __name__ == "__main__":
    main()