
import data_loader 
import sqlite3
import pandas as pd
import stock_utils
from pathlib import Path

#interface script for data_loader


#takes a list, tuple, set, pd series, and dictionary and extracts strings only
def string_only(*args, **kwargs) -> list[str]:
    a = []
    if isinstance(args, pd.Series):
        print("under c")
    else:
        def extract_string(obj):
            if isinstance(obj, str):
                a.append(obj)
            elif isinstance(obj, (list, tuple, set)):
                for x in obj:
                    extract_string(x)
        extract_string(args)

    print(f"a is {a}")
    return a


#can take a list, tuple, dictionary, set, df.series of input and calls get_stock() for each element in the argument
#user can set col_name to specify name to be checked in db
def load_multiple_tickers(data, *args, **kwargs) -> list['myclass']:
    b : list = []
    c : list[stock_utils.Stock] = [stock_utils.Stock()]
    try:
        if isinstance(data, str) and data.endswith('.db'):
            try:
                p = Path(data).expanduser()
                with sqlite3.connect(str(p)) as conn:
                    curr = conn.cursor()
                    curr.execute("""SELECT name FROM sqlite_master Where type='table';""")
                    tables = curr.fetchall()
                    for table in tables:

                        curr.execute(f"SELECT * from {str(table[0])}")
                        a = curr.fetchall()
                        b.extend(string_only(*a))
            except:
                print(f"the file was not found in {p}")
        else:
            b.extned(data)
        if isinstance(args, (list,tuple,set)):
            b.extend(string_only(args))
    except:
        print(f"ERROR: NO TICKERS ARE FOUND")
    c: list[stock_utils.Stock] = [
    stock for ticker in b
    if (stock := stock_utils.Stock.from_ticker(ticker)) is not None
    ]
    return c