#stock_utilis gets data from data_loader and stores/handles data

import pandas as pd
import data_loader
class Stock:
    def __init__(self):
        self.df = pd.DataFrame()         # Main stock data
        self.other_df = pd.DataFrame()   # Additional info

    def avg_approximation(self):
        if not self.df.empty:
            self.df['VWAP_Price'] = self.df[['Open', 'Close', 'High', 'Low']].sum(axis=1) / 4
            self.df['Volatility'] = (abs(self.df['VWAP_Price'] - self.df['High']) 
                                     + abs(self.df['VWAP_Price'] - self.df['Low']))
            grouped = self.df.groupby(pd.Grouper(key='Datetime', freq='30T', origin='start_day', offset=pd.Timedelta(hours=9)))
            self.other_df = grouped['Volatility'].mean().reset_index().rename(columns={'Volatility': 'Avg_volatility'})

        else:
            print("DataFrame is empty")

    @classmethod
    def from_ticker(cls, ticker):
        obj = cls()
        obj.df = data_loader.get_stock(ticker)
        return obj

    
    