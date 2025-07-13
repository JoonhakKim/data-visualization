import sqlite3
import pandas as pd
import yfinance as yf

# Fetch data
asml = yf.Ticker("asml")
asml_info = asml.info

# Convert dict values that are lists/dicts to strings
cleaned_info = {k: str(v) if isinstance(v, (list, dict)) else v for k, v in asml_info.items()}

# Turn into DataFrame
df = pd.DataFrame([cleaned_info])

# Save to SQLite
conn = sqlite3.connect("stocks.db")
df.to_sql("asml_info", conn, if_exists="replace", index=False)
conn.close()
