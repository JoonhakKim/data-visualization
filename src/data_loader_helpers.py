
import sqlite3
import pandas as pd
from pathlib import Path

from . import stock_utils
from . import data_loader




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


#can take a list, tuple, dictionary, set, df.series of input and calls get_price() for each element in the argument
#user can set col_name to specify name to be checked in db
def update_tickers(data, *args, **kwargs) -> list[stock_utils.Stock]:
    b : list = []
    c : list[stock_utils.Stock] = [stock_utils.Stock()]
    try:
        if isinstance(data, str) and data.endswith('.db'):
            try:
                #get the path value for the user's local db
                path = Path(data).expanduser() 
                with sqlite3.connect(str(path)) as conn:
                    curr = conn.cursor()
                    #if the .db file is given as an input, it checks all the values within the file.
                    #maybe i should make an argument that let the user specify the info
                    curr.execute("""SELECT name FROM sqlite_master Where type='table';""")
                    tables = curr.fetchall()
                    for table in tables:

                        curr.execute(f"SELECT * from {str(table[0])}")
                        a = curr.fetchall()
                        b.extend(string_only(*a))
            except:
                print(f"the file was not found in {p}")
        else:
            b.append(data)
        if isinstance(args, (list,tuple,set)):
            b.extend(string_only(args))
    except:
        print(f"ERROR: NO TICKERS ARE FOUND")

    
    c: list[stock_utils.Stock] = [
    stock for ticker in b
    #wallus operator is not rly necessary here. 
    if (stock := stock_utils.Stock.from_ticker(ticker)) is not None
    ]
    return c


def load_multipler_ticker(data, *args, **kwargs) -> list[stock_utils.Stock]:
    str_list : list = []
    class_list : list[stock_utils.Stock] = [stock_utils.Stock()]

    try:
        if isinstance(data, str) and data.endswith('.db'):
            try:
                #get the path value for the user's local db
                path = Path(data).expanduser() 
                with sqlite3.connect(str(path)) as conn:
                    curr = conn.cursor()
                    curr.execute("""SELECT name FROM sqlite_master Where type='table';""")
                    tables = curr.fetchall()
                    for table in tables:
                        curr.execute(f"SELECT * from {str(table[0])}")
                        a = curr.fetchall()
                        str_list.extend(string_only(*a))
            except:
                print(f"the file was not found in {p}")
        else:
            str_list.append(data)
        if isinstance(args, (list, tuple,set)):
            str_list.extend(string_only(args))
    except:
        print(f"ERROR: NO TICKERS ARE FOUND")

    class_list = [
        stock
        for ticker in str_list
        if (stock := stock_utils.Stock.db_from_ticker(ticker)) is not None
    ]
    print("aaa" if class_list is not None else "bbb")
    return class_list