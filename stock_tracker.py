import requests
import yfinance as yf


# -----------------------------
# CONFIG
# -----------------------------
STOCKS = ["AAPL", "GOOGL", "TSLA"]

BUY_PRICES = {
    "AAPL": 100.0,
    "GOOGL": 3000.0,
    "TSLA": 700.0
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
    buy_price = BUY_PRICES[symbol]
    return current_price - buy_price


# -----------------------------
# MAIN LOGIC
# -----------------------------
def main():
    print("Stock Tracker Running...\n")

    for stock in STOCKS:
        current_price = get_stock_price(stock)
        pnl = calculate_profit_loss(stock, current_price)

        print(f"{stock}: Current Price = {current_price: .2f}, P/L = {pnl: .2f}")


if __name__ == "__main__":
    main()