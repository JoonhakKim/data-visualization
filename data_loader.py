import yfinance as yf
from datetime import datetime
import pandas as pd

def get_intraday_prices():
    # Step 1: Ask user for inputs
    ticker = input("Enter company ticker (e.g., AAPL): ").upper()
    start_date_str = input("Enter start date (MM/DD/YYYY): ")
    end_date_str = input("Enter end date (MM/DD/YYYY): ")
    interval = input("Enter time interval (e.g., 1m, 5m, 15m, 30m, 1h): ")

    # Step 2: Convert dates
    try:
        start_date = datetime.strptime(start_date_str, "%m/%d/%Y").strftime("%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%m/%d/%Y").strftime("%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Use MM/DD/YYYY.")
        return

    # Step 3: Download data
    try:
        df = yf.download(
            tickers=ticker,
            start=start_date,
            end=end_date,
            interval=interval,
            progress=False
        )
    except Exception as e:
        print("Error fetching data:", e)
        return

    if df.empty:
        print("No data found for given parameters.")
        return

    # Step 4: Extract close prices into a list
    price_list = df['Close'].tolist()

    # Step 5: Display results
    print(f"\n{len(price_list)} prices found from {start_date} to {end_date} for {ticker} at {interval} interval.")
    print("First 5 prices:", price_list[:5])
    return price_list

# Run if script is executed
if __name__ == "__main__":
    get_intraday_prices()
