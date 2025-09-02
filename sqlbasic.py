
import sqlite3
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from src import stock_utils
from src import data_loader_helpers
from src import data_loader
from src import data_visualizer as data_visualizer



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

c: list[stock_utils.Stock] = []

c.extend(data_loader_helpers.load_multipler_ticker("META"))
#c.extend(data_loader_helpers.update_tickers("META"))
c.extend(data_loader_helpers.update_tickers("AMZN"))
data_visualizer.plot_daily_3d(df = c[1].df, data_type = 'Close', chart_type= 'bar')

#c[0].avg_approximation()
#c[1].avg_approximation()
#data_visualizer.plot_daily_3d(df = c[0].df, data_type = 'Close', chart_type= 'bar')
#data_visualizer.plot_daily_3d(df = c[1].df, data_type = 'Close', chart_type= 'scatter')
#data_visualizer.plot_daily_3d(df = c[2].df, data_type = 'Close', chart_type= 'line')