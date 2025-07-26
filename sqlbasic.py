from __init__ import pd, sqlite3, yf
import data_loader
import stock_utils
import numpy as np
import matplotlib.pyplot as plt
#Stock market price analysing program for 
#1. day trading (1 day frame )
#1. a week trading (a week frame)
# n weeks trading on average 3.5 weeks up to 7 week
#data_loader contains fetcher functions to fetch data from yahoo finance and convert it to local data base.
#data_manager contains functions to calculate local data and store information into local data base
#stock_utilis gets data from local sql mainly data_manager and use data to calculate numeric values
#stock_adjuster learns from previous prediction and adjust weights
#weight_exporter stores learned weight and save them to local server 
#data_exporter contains helper function to convert numeric, python data to sql data and store into local data base
#visualizer.py contains functions to visualize python data. 

data_loader.create_db()
mystock = stock_utils.Stock.from_ticker("AMZN")
