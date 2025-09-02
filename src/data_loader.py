import pandas as pd
import sqlite3
import yfinance as yf
import sys
import numpy as np
import contextlib
import pytz

from datetime import datetime, timedelta
from pathlib import Path
from src import file_path, db_path






#the functions here are supposed to be used directly but rather indirectly by calling those functions in _helper.py


#################SOME STRING VALUES#################
####################################################

earliest_date_query_template = "SELECT Datetime FROM price_data WHERE ticker = '{name}' ORDER BY Datetime ASC LIMIT 1;"
latest_date_query_template = "SELECT Datetime FROM price_data WHERE ticker = '{name}' ORDER BY Datetime DESC LIMIT 1;"
data_query_template1 = "SELECT * FROM PRICE_DATA WHERE ticker = '{name}' ORDER BY Datetime ASC"
data_query_template = "SELECT * FROM PRICE_DATA WHERE ticker = '{name}' AND Datetime > '{min_Datetime}'ORDER BY Datetime ASC"


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

# This function retrieves historical stock data from Yahoo Finance using yfinance (yf),
# and updates the data into a local SQLite database.
def get_stock_from_yf(ticker_name: str) -> pd.DataFrame:
    ticker_name = ticker_name.upper()
    if ticker_exists(ticker_name) == False:
        return None
    else:

        #call yf ticker information.
        temp_ticker = yf.Ticker(ticker_name)   
        temp_data = temp_ticker.history(period="60d", interval="5m")[['Open', 'Close', 'High', 'Low', 'Volume']]
        temp_data['ticker'] = ticker_name
        temp_data = temp_data.reset_index().set_index(['ticker', 'Datetime'])
        #since yf automatically make the dateframe timezone aware, drop the timezone since the program doesn't really need it
        temp_data.index = temp_data.index.set_levels(temp_data.index.levels[1].tz_localize(None), level=1)

        #check whether data exists in local stock.db
        with sqlite3.connect(db_path + '/stock_price.db') as temp_conn:
            try:
                #query the recent and last date to compare
                # I could have made a get_earliest_date() function,
                # but it would prevent using a 'with' statement for the DB connection and add extra process.
                temp_cursor = temp_conn.cursor()
                date_query = earliest_date_query_template.format(name=ticker_name)
                temp_cursor.execute(date_query)
                db_earlist_date = pd.to_datetime(temp_cursor.fetchone()[0], errors = 'coerce')
                filtered = temp_data[temp_data.index.get_level_values('Datetime') < db_earlist_date]
                i = filtered.index[-1] if not filtered.empty else None
                if not i:
                    print(f" DB is already up-to-date for {ticker_name}")
                    return temp_data

                temp_data = temp_data.loc[:i]

                temp_data.to_sql('price_data', temp_conn, if_exists='append', index=True)
                print(f"the earlist date in data base: {db_earlist_date}, Earliest date requiring update: {filtered.index[0]}")
                print(f" Inserted {len(temp_data)} new rows for {ticker_name}")
            except:
                try:
                    temp_data.to_sql('price_data', temp_conn, if_exists = 'append', index =True, index_label =['ticker', 'Datetime'])
                    print(f"Data has been successfully saved to the local stocks.db for {ticker_name}")
                except:
                    print(f"ERROR: UNABLE TO INSERT DATA INTO stock_price.db at {db_path}")
                    print("stock_price.db file might have been damaged please run the repair function")
                    return None
            
    return temp_data

def load_stock_from_db(ticker_name, length : str = '60d') -> pd.DataFrame:
    ticker_name = ticker_name.upper()
    if ticker_exists(ticker_name) == False:
        return None
    else:
        try:
            with sqlite3.connect(db_path + "/stock_price.db") as conn:
                curr = conn.cursor()
                # Get latest and current dates from DB
                latest_date_query = latest_date_query_template.format(name=ticker_name)
                current_date_query = earliest_date_query_template.format(name=ticker_name)

                curr.execute(latest_date_query)
                latest_date = pd.to_datetime(curr.fetchone()[0], errors='coerce')

                curr.execute(current_date_query)
                current_date = pd.to_datetime(curr.fetchone()[0], errors='coerce')
                time_diff = latest_date - current_date

                # If the gap is too small (data is missing), pull all data
                if time_diff < pd.Timedelta(length):
                    print("Data is missing, pulling all available data.")
                    a = pd.read_sql_query(data_query_template1.format(name=ticker_name), conn)
                else:
                    des_datetime = current_date - pd.Timedelta(length)
                    a = pd.read_sql_query(
                        data_query_template.format(name=ticker_name, min_Datetime=des_datetime), conn)
                
                #since the program won't automatically recognize multi-indexes, 
                a = a.reset_index().set_index(['ticker', 'Datetime'])
                print(type(a.index.get_level_values('Datetime')))
                return a
        except:
            print(f"ERROR: UNABLE TO OPEN stock_price.db file at {db_path}")
            return None
 
