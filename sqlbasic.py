import sqlite3
import pandas as pd
import yfinance as yf



#'''def main():
#if __name__ == "__main()__": main()

pd.set_option('display.max_columns', None)  # Show all columns
# Connect to your existing database
conn = sqlite3.connect("stocks.db")
# Fetch data
user_input = input("Enter the name of the company: " )

try:
    asml = yf.Ticker("asml")
except ValueError as e:
    print(f"Error: {e}")


asml_info = asml.info
#get info
df = pd.read_sql("SELECT * FROM asml_info", conn)


#market cap = # amount of stock share
# total revenue = # total income
# gross profits = #T.R - cost of Goods sold
#EBITDA := earning before interest := EBIT + Depreciation + Amortization 
#How profitable the company is from its actual business, ignoring:
# Interest (debt decisions) Taxes (which vary by country) 
# Depreciation & Amortization (non-cash accounting expenses)
#return onEquity: "If I give this company $1 of my money, how much profit does it make with it?" ( Net Income / Shareholders' Equity)


key_columns = [
    'marketCap', 'enterpriseValue', 'totalRevenue', 'grossProfits', 'netIncomeToCommon',
    'ebitda', 'freeCashflow', 'operatingCashflow', 'totalDebt', 'bookValue',
    'trailingPE', 'forwardPE', 'priceToBook', 'priceToSalesTrailing12Months', 'trailingPegRatio',
    'profitMargins', 'grossMargins', 'operatingMargins', 'ebitdaMargins',
    'earningsGrowth', 'revenueGrowth', 'returnOnAssets', 'returnOnEquity',
    'dividendRate', 'dividendYield', 'payoutRatio',
    'regularMarketPrice', 'volume', 'averageVolume', 'bid', 'ask',
    'fiftyTwoWeekHigh', 'fiftyTwoWeekLow', 'fiftyDayAverage', 'twoHundredDayAverage',
    'shortRatio', 'sharesShort', 'heldPercentInstitutions'
]
# Load the ticker (e.g., ASML)
ticker = yf.Ticker("ASML")

# Get 1-minute interval data for the last 7 days (max allowed)
data = ticker.history(period="7d", interval="1m")

print(type(data))










# Select only those columns that exist in your DataFrame
existing_columns = [col for col in key_columns if col in df.columns]
df_filtered = df[existing_columns]
#print(df_filtered)







cleaned_info = {k: str(v) if isinstance(v, (list, dict)) else v for k, v in asml_info.items()}

# Turn into DataFrame
df = pd.DataFrame([cleaned_info])

# Save to SQLite
conn = sqlite3.connect("stocks.db")

# ✅ Write the cleaned DataFrame into SQL FIRST
df.to_sql("asml_info", conn, if_exists="replace", index=False)

# ✅ Now read it back from the SQL database (optional)
df_sql = pd.read_sql("SELECT * FROM asml_info", conn)

# Display for debug (optional)
#print(df_sql.head(3))
# Display
conn.close()

