import requests
import yfinance as yf


# -----------------------------
# CONFIG (fill later)
# -----------------------------
STOCKS = ["AAPL", "GOOGL", "TSLA"]

BUY_PRICES = {
    "AAPL": 150.0,
    "GOOGL": 2500.0,
    "TSLA": 700.0
}

# -----------------------------
# FETCH PRICE (placeholder)
# -----------------------------
def get_stock_price(symbol):

    """Fetch the current stock price using yfinance"""
    stock = yf.Ticker(symbol)
    
    # Get current price from the last trading day
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

        print(f"{stock}: Current Price = {current_price}, P/L = {pnl}")


if __name__ == "__main__":
    main()