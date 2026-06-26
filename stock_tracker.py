import yfinance as yf
import pandas as pd #handles data perfectly in tabular data. easy to export to excel.


# -----------------------------
# CONFIG
# -----------------------------


#price is shown in usd because API return prices in native exchange currency of the stock. 
STOCKS = ["AAPL", "GOOGL", "TSLA", "AMZN", "MSFT", "NKE", "META"]

BUY_PRICES = {
    "AAPL": 100.0,
    "GOOGL": 3000.0,
    "TSLA": 700.0,
    "AMZN": 300.0,
    "MSFT": 250.0,
    "NKE": 150.0,
    "META": 350.0
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

        #if data is not found, return 0 and print a message.
        if history.empty:
            print(f"No data found for {symbol}.")
            return 0

    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return 0

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

    if current_price == 0:
        print(f"Skipping {stock} due to missing data.")
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
    print("Excel report generated: stock_tracker.xlsx\n")

if __name__ == "__main__":
    main()