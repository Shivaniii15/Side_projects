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
STOCKS = ["AAPL", "GOOGL", "TSLA", "AMZN", "MSFT", "NKE", "METAA"]

BUY_PRICES = {
    "AAPL": 100.0,
    "GOOGL": 3000.0,
    "TSLA": 700.0,
    "AMZN": 300.0,
    "MSFT": 250.0,
    "NKE": 150.0,
    "METAA": 350.0
}

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

#make the excel file and save it to the current directory.
#overwrites existing one
df.to_excel("stock_tracker.xlsx", index=False)


def main():
    print("Stock Tracker Report Generated: stock_tracker.xlsx")
    logging.info("Excel report generated: stock_tracker.xlsx\n")

if __name__ == "__main__":
    main()