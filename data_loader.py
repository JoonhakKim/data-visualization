from __init__ import pd, sqlite3, yf
import sys
import numpy as np
import contextlib
from datetime import datetime, timedelta
import pytz

date_query_template = "SELECT Datetime FROM {table} ORDER BY datetime ASC LIMIT 1"
#"SELECT Datetime FROM AAPL ORDER BY Datetime ASC LIMIT 1"

insert_stock_info = """
INSERT INTO TICKER (TIME, Open, Close, High, Low, Volume )
"""


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
    with sqlite3.connect("ticker_list.db") as temp_conn:
        temp_cursor = temp_conn.cursor()
        temp_cursor.execute("""CREATE TABLE IF NOT EXISTS ticker (
                        ticker TEXT PRIMARY KEY
                    )""")
    with sqlite3.connect("stock_price.db") as temp_conn:
        temp_cursor = temp_conn.cursor()
        temp_cursor.execute("""CREATE TABLE IF NOT EXISTS Dummy (
                Datetime TEXT NULL,
                Ticker TEXT DUMMY,
                Price TEXT NULL,
                Open TEXT NULL,
                Close TEXT NULL,
                Volume TEXT NULL
            )""")
        temp_conn.commit()
        
    with sqlite3.connect("stock_info.db") as temp_conn:
        temp_cursor = temp_conn.cursor()
        temp_cursor.execute("""CREATE TABLE IF NOT EXISTS Dummy (
                            Ticker TEXT DUMMY
                            PER INT NULL,
                            PBR INT NULL,
                            MARKET_SHARE INT NULL
                            )
            """)
    with sqlite3.connect("weights.db") as temp_conn:
        temp_cursor.execute("""CREATE TABLE IF NOT EXISTS ticker (
            ticker TEXT PRIMARY KEY
        )""")
    return None

#check whether ticker exist in local .db, 
def ticker_exists(name_to_check: str) -> bool:
    with sqlite3.connect("ticker_list.db") as temp_conn:
        temp_cursor = temp_conn.cursor()
        temp_cursor.execute("""CREATE TABLE IF NOT EXISTS ticker (
                        ticker TEXT PRIMARY KEY
                    )""")
        temp_cursor.execute("SELECT 1 FROM ticker WHERE ticker = ? LIMIT 1", (name_to_check,))
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
                    temp_cursor.execute("INSERT INTO ticker (ticker) VALUES (?)", (name_to_check,))
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




#this function gets stock value from yf, and store it into local python list and update to sql.
def get_stock(name_ticker: str) -> pd.DataFrame:
    name_ticker = name_ticker.upper()
    if ticker_exists(name_ticker) == False:
        print(f"Ticker Not found")
        return None
    else:

        temp_ticker = yf.Ticker(name_ticker)   # This is a Ticker object
        temp_data = temp_ticker.history(period="30d", interval="5m")[['Open', 'Close', 'High', 'Low', 'Volume']]
        temp_data = temp_data.reset_index()

        ####
        #check whether data exists in local stock.db
        with sqlite3.connect('stock_price.db') as temp_conn:
            try:
                #query the recent and last date to compare
                temp_cursor = temp_conn.cursor()
                date_query = date_query_template.format(table=name_ticker)
                temp_cursor.execute(date_query)

                db_latest_date = pd.to_datetime(temp_cursor.fetchone()[0], format = '%Y-%m-%d %H:%M:%S%z')
                
                filtered = temp_data[pd.to_datetime(temp_data['Datetime']) <= db_latest_date]
                i = filtered.index[-1] if not filtered.empty else None
                
                if not i:
                    print(f" DB is already up-to-date for {name_ticker}")
                    return temp_data
                
                temp_data = temp_data.loc[0: i]
                print(temp_data)
                temp_data.to_sql(name_ticker, temp_conn, if_exists='append', index=False)
                print(f" Inserted {len(temp_data)} new rows for {name_ticker}")


            except:
                try:
                    temp_data.to_sql(name_ticker, temp_conn, if_exists = 'append', index =False)
                except:
                    print("ERROR: UNABLE TO INSERT DATA INTO .DB")
                    print("stock_price.db file might have been damaged please run the repair function")
            
    return temp_data
        


