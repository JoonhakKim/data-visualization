from pathlib import Path
from datetime import datetime
import sqlite3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from mpl_toolkits.mplot3d import Axes3D


from src import file_path, db_path

#Path_Data 
#ss


'''
daily goal: rename variables!! and fix the structure for the readbility 
#daily plot_3d: 
    make an argument that takes graph type: bar and candle
    make an argument that helps the user to adjust the number of data to be plot
#
'''

def is_valid_date(date_str: str) -> bool:
    #None is a valid input to handle default cases
    if date_str is None:
        return True  
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False
    

def is_date_out_of_range(start_day: str, end_date: str, start_day1:str, end_date1:str):
    return

#
#with sqlite3.connect(db_path + '/stock_price.db') as conn:


def constructor(fig_size = 'auto',
                min_value = 'auto', max_value = 'auto', 
                xticks = 'auto', yticks = 'auto', zticks = 'auto',) -> plt.figure :    
    

    fig = plt.figure(figsize=(12, 6))  
    ax = fig.add_subplot(121, projection='3d')
    ax1 = fig.add_subplot(122, projection = '3d')

    # Major locator intervals
    ax.xaxis.set_major_locator(MultipleLocator(10))
    ax.yaxis.set_major_locator(MultipleLocator(10))
    # Tick label size
    ax.tick_params(axis='x', labelsize=12)
    ax.tick_params(axis='y', labelsize=12)
    ax.set(
        zlim=(min_value, series.max()),
        xlabel='Time',
        ylabel='Date',
        zlabel=data_type, 
        xticks = time_idx, 
        yticks = range(len(date_range)),
        xticklabels = [t.strftime('%H:%M') for t in time_range],
        yticklabels = [d.strftime('%m-%d') for d in date_range]
    )


#this function takes panda data frame, and group it by days 
def plot_daily_3d(df : pd.DataFrame, data_type: str, interval: str = '5min', 
                  start_day: str = None, end_day: str = None, Parse = '60d', chart_type = 'line'):

    #check parmeters 
    if not is_valid_date(start_day) or not is_valid_date(end_day):
        raise ValueError("Error: start_day or end_day is not a valid date")

    if chart_type not in ('bar', 'line', 'scatter'): #check valid argument
        raise ValueError("Error: chart_type is invalid")
    
    ticker = df.index.get_level_values('ticker')
    series = df[data_type].droplevel("ticker") #dropping 'ticker' index 
    print(series)


    #get earlest, latest day by accessing the first and the last index.
    #series.index.min() would be safer but in this case, is not necessary because series is sorted already.
    earliest_day = series.index[0]
    latest_day = series.index[-1]
    '''
    if earliest_day > pd.to_datetime(start_day):
        raise ValueError(f"Error: start_day out of range. The earliest date in the given data is {earliest_day}")

    if latest_day < pd.to_datetime(start_day):
        raise ValueError(f"Error: latest_day out of range. The earliest date in the given data is {earliest_day}")
    '''    
    grouped = series.groupby(series.index.date) #sort data by each date.

    time_range = pd.date_range("09:00", "16:00", freq= interval).time
    date_range = series.index.normalize().unique() #normalize => get rid of time stamp, unique => remove duplicates.
    #[[]]:= data frame, `[]:= series`
    
    fig = plt.figure(figsize=(12, 8))  
    ax = fig.add_subplot(projection='3d')

    time_idx = np.arange(len(time_range)) #indexing time, not actual timestamp from 0 to around 75.
    min_value = series.min() #extract min_value to avoid calling series.min() multiple times

    ax.set(
        zlim=(min_value, series.max()),
        xlabel='Time',
        ylabel='Date',
        zlabel=data_type, 
        xticks = time_idx, 
        yticks = range(len(date_range)),
        xticklabels = [t.strftime('%H:%M') for t in time_range],
        yticklabels = [d.strftime('%m-%d') for d in date_range]
    )


    #plot(left, height, zs(zcoordinates), zdir)
    i=0 #convenient index variable for shifting across the grid
    if chart_type == 'line':
        for idx, value in grouped: 
            arr = value.to_numpy()
            ax.plot(time_idx[:len(arr)], arr, zs = i, zdir= 'y', color = 'red', alpha = 0.4)
            i += 1
    elif chart_type == 'bar':
        for idx, value in grouped: 
            arr = value.to_numpy()
            #arr-min_value substract all values in series by min_value, and set bottomn = min_value to shift
            #could it be better way to plot bars? it seems a bit unnecessary computation :<
            ax.bar(time_idx[:len(arr)], arr- min_value, zs = i, zdir= 'y', 
                   color = 'red', alpha = 0.4, bottom=min_value, edgecolor='black')
            i += 1
    elif chart_type == 'scatter':
        for idx, value in grouped: 
            arr = value.to_numpy()
            ax.scatter(time_idx[:len(arr)], i, arr, marker = 'o', s = 0.4)
            i += 1
    else:
        raise ValueError("chart_type is invalid")



    # Major locator intervals
    ax.xaxis.set_major_locator(MultipleLocator(10))
    ax.yaxis.set_major_locator(MultipleLocator(10))
    # Tick label size
    ax.tick_params(axis='x', labelsize=12)
    ax.tick_params(axis='y', labelsize=12)
    plt.tight_layout()
    
    plt.show()
    plt.close()
    #y1 = B0+b1x1+ B2x^2 +e1

