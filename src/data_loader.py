import pandas as pd
import sqlite3
import yfinance as yf
import sys
import numpy as np
import contextlib
from datetime import datetime, timedelta
import pytz
from pathlib import Path




#################SOME STRING VALUES#################
####################################################
file_path = Path(__file__).resolve().parent
db_path = str(file_path.parents[0] / 'Database')

date_query_template = "SELECT Datetime FROM price_data WHERE ticker = '{ticker_name}' ORDER BY Datetime ASC LIMIT 1;"
#"SELECT Datetime FROM AAPL ORDER BY Datetime ASC LIMIT 1"
insert_meta_stock_info = """
INSERT INTO meta_data (ticker, name, sector, exchange)
"""

insert_stock_info = """
INSERT INTO TICKER (ticker, Datetime, Open, Close, High, Low, Volume )
"""
#######################################################
#######################################################

def log_stdout_stderr_to():
    with open("yfErrorLog", 'a') as log_file:
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        sys.stdout = log_file
        sys.stderr = log_file
        try:
            yield
        finally:
            sys.stdout = original_stdout
            sys.stderr = original_stderr

def create_db():
    with sqlite3.connect(db_path + "/ticker_list.db") as temp_conn:
        temp_cursor = temp_conn.cursor()
        temp_cursor.execute("""CREATE TABLE IF NOT EXISTS ticker_list (
                        ticker TEXT PRIMARY KEY
                    )""")
        temp_conn.commit()
    with sqlite3.connect(db_path + "/stock_price.db") as temp_conn:
        temp_cursor = temp_conn.cursor()
        temp_cursor.execute("""CREATE TABLE IF NOT EXISTS meta_data (
                            ticker TEXT PRIMARY KEY,
                            name TEXT,
                            sector TEXT,
                            exchange TEXT
                            )
        """
        )
        temp_cursor.execute("""
            CREATE TABLE IF NOT EXISTS price_data (
                ticker TEXT,
                Datetime TEXT,
                Open REAL,
                Close REAL,
                Low REAL,
                High REAL,
                Volume INTEGER,
                volatility REAL,
                PRIMARY KEY (ticker, Datetime)
            )""")
        temp_cursor.execute("""
            CREATE TABLE IF NOT EXISTS indicator_data (
                    ticker TEXT,
                    Datetime TEXT,
                    rsi REAL,
                    macd REAL,
                    sma_50 REAL,
                    sma_200 REAL,
                PRIMARY KEY (ticker, Datetime)
            )""")
        temp_conn.commit()
        
    with sqlite3.connect(db_path + "/stock_info.db") as temp_conn:
        temp_cursor = temp_conn.cursor()
        temp_cursor.execute("""CREATE TABLE IF NOT EXISTS Dummy (
                            ticker TEXT DUMMY
                            PER INT NULL,
                            PBR INT NULL,
                            share INT NULL
                            )
            """)
        temp_conn.commit()
    with sqlite3.connect(db_path + "/weights.db") as temp_conn:
        temp_cursor.execute("""CREATE TABLE IF NOT EXISTS ticker (
            ticker TEXT PRIMARY KEY
        )""")
        temp_conn.commit()
    return None

#check whether ticker exist in local .db, 
def ticker_exists(name_to_check: str) -> bool:
    with sqlite3.connect(db_path + "/ticker_list.db") as temp_conn:
        temp_cursor = temp_conn.cursor()
        temp_cursor.execute("SELECT 1 FROM ticker_list WHERE ticker = ? LIMIT 1", (name_to_check,))
        result = temp_cursor.fetchone()
        #if ticker name doesn't exist in local db,
        #check ticker from the yf finance and update it
        if result is None:
            try:
                temp_info = yf.Ticker(name_to_check).info
                if temp_info.get("regularMarketPrice") is None:
                    print(f"Ticker '{name_to_check}' not found in Yahoo Finance.")
                    return False
                else:
                    #updata local db
                    temp_cursor.execute("INSERT INTO ticker_list (ticker) VALUES (?)", (name_to_check,))
                    temp_conn.commit()
                    return True
            except ValueError as err:
                print(f"Error:  {err}")
                return False
    return result is not None


#this function update information from yf finance and store it into local_db
"""def update_stock(ticker_name : str) -> bool:
    ticker_name.upper()
    if not ticker_exists():
        print(f"Ticker not found")
        return False
    else:
        temp_ticker = yf.Ticker(ticker_name)
        temp_"""


# This function retrieves historical stock data from Yahoo Finance using yfinance (yf),
# and updates the data into a local SQLite database.
# It is particularly useful for fetching long-term static data (e.g., more than one day)
# for comparative analysis or backtesting purposes.
# often used only for the first time retriving a stock info.
def get_stock(name_ticker: str) -> pd.DataFrame:
    name_ticker = name_ticker.upper()
    if ticker_exists(name_ticker) == False:
        return None
    else:

        #call yf ticker information.
        temp_ticker = yf.Ticker(name_ticker)   
        temp_data = temp_ticker.history(period="60d", interval="5m")[['Open', 'Close', 'High', 'Low', 'Volume']]
        temp_data['ticker'] = name_ticker
        temp_data = temp_data.reset_index().set_index(['ticker', 'Datetime'])
        #since yf automatically make the dateframe timezone aware, drop the timezone since the program doesn't really need it
        temp_data.index = temp_data.index.set_levels(temp_data.index.levels[1].tz_localize(None), level=1)


        #check whether data exists in local stock.db
        with sqlite3.connect(db_path + '/stock_price.db') as temp_conn:
            try:
                #query the recent and last date to compare
                temp_cursor = temp_conn.cursor()
                date_query = date_query_template.format(ticker_name=name_ticker)
                temp_cursor.execute(date_query)
                db_earlist_date = pd.to_datetime(temp_cursor.fetchone()[0], errors = 'coerce')
                filtered = temp_data[temp_data.index.get_level_values('Datetime') < db_earlist_date]
                i = filtered.index[-1] if not filtered.empty else None
                if not i:
                    print(f" DB is already up-to-date for {name_ticker}")
                    return temp_data

                temp_data = temp_data.loc[:i]

                temp_data.to_sql('price_data', temp_conn, if_exists='append', index=True)
                print(f"the earlist date in data base: {db_earlist_date}, Earliest date requiring update: {filtered.index[0]}")
                print(f" Inserted {len(temp_data)} new rows for {name_ticker}")
            except:
                try:
                    temp_data.to_sql('price_data', temp_conn, if_exists = 'append', index =True, index_label =['ticker', 'Datetime'])
                    print(f"Data has been successfully saved to the local stocks.db for {name_ticker}")
                except:
                    print(f"ERROR: UNABLE TO INSERT DATA INTO stock_price.db at {db_path}")
                    print("stock_price.db file might have been damaged please run the repair function")
                    return None
            
    return temp_data


# This function loads stock data only from the local SQLite database,
# without making any requests to Yahoo Finance.
# It is useful when the data for the desired date range has already been stored and updated.
#def load_stock_from_db():
    #with sqlite3.connect(db_path + "/stock.price.db"):




# This function checks whether the local database is up to date, based on the specified interval:
# - If 'day' is provided, it returns True as long as stock data exists for that date.
# - If 'minute' is provided, it returns True only if the stored data aligns with the latest available data.
# Default behavir is dat.
#def check_updated(interval: str = 'day') -> bool:
    #if interval not in ['day', 'minute']:
        #raise ValueError("Interval must be either 'day' or 'minute'")
    

