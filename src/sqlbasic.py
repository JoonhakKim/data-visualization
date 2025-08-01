from __init__ import pd, sqlite3, yf
import stock_utils
import numpy as np
import matplotlib.pyplot as plt
import data_loader_helpers
import data_loader
import streamlit as st
import pandas as pd




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


#data_loader_helpers.load_multiple_tickers("AMZN")
data_loader.create_db()
data_loader.get_stock("META")
c: list[stock_utils.Stock] = [stock_utils.Stock()]
c= data_loader_helpers.load_multiple_tickers("example.db")
#print(type(c))
print(c)      # Should be 'Stock(some_name)' if __repr__ works
#data_loader_helpers.load_multiple_tickers('AMZN', 'AAPL', 'APPL')
df = c[0].df.reset_index()
st.bar_chart(df.set_index('Datetime')['Volume'])

start_day = pd.Timestamp(c[0].df.index.get_level_values("Datetime").min().date())
end_day = pd.Timestamp(c[0].df.index.get_level_values("Datetime").max().date())
current_day = start_day
#print(current_day)
#print(start_day)
#print(end_day)
'''
idx = pd.IndexSlice # Create an object to more easily perform multi-index slicing.
while current_day<= end_day:
    start_time = current_day + pd.Timedelta(hours=9, minutes=30)
    end_time = current_day + pd.Timedelta(hours=16)
    day_data = c[0].df.loc[idx[:, start_time:end_time], :]
    print(f"ssdsd: {day_data}")
    current_day += pd.Timedelta(days = 1)



plt.figure(figsize=(10, 5))
dates = c[0].df.index.get_level_values('Datetime')
plt.plot(dates, c[0].df['Close'])  # assuming 'Close' is your y-axis
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.title('Stock Price Over Time')
plt.xticks(rotation=45)  # optional: rotate dates
plt.tight_layout()
plt.show()'''