import requests
import yfinance as yf
import pandas as pd #handles data perfectly in tabular data. easy to export to excel.


# -----------------------------
# CONFIG
# -----------------------------

#price is shown in usd because API return prices in native exchange currency of the stock. 
STOCKS = ["AAPL", "GOOGL", "TSLA", "AMZN", "MSFT", "NKE", "FB"]

BUY_PRICES = {
    "AAPL": 100.0,
    "GOOGL": 3000.0,
    "TSLA": 700.0,
    "AMZN": 300.0,
    "MSFT": 250.0,
    "NKE": 150.0,
    "FB": 350.0
}

# -----------------------------
# FETCH PRICE 
# -----------------------------
def get_stock_price(symbol):

    """Fetch the current stock price using yfinance"""
    #connection to yahoo finance API.
    stock = yf.Ticker(symbol)
    
    """Get current price from the last trading day"""
    #history(period="1d") gets today's data, and "Close" gives the closing price. iloc[-1] gets the latest price.
    current_price = stock.history(period="1d")["Close"].iloc[-1];
    return current_price

    
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
    pnl = calculate_profit_loss(stock, current_price)

    data.append({
        "Stock": stock,
        "Buy Price": BUY_PRICES.get(stock, 0),
        "Current Price": round(current_price, 2),
        "P/L": round(pnl, 2)
})

df = pd.DataFrame(data)

df.to_excel("stock_tracker.xlsx", index=False)


def main():
    print("Excel report generated: stock_tracker.xlsx\n")

if __name__ == "__main__":
    main()