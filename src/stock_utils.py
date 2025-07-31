#stock_utilis gets data from data_loader and stores/handles data

import pandas as pd
import data_loader


class Stock:
    def __init__(self):
        # 'df' contains all raw numerical data (excluding percentage changes)
        # 'other_df' contains derived metrics like percentage changes (e.g., deltas)
        self.df = pd.DataFrame()         # Main stock data
        self.delta_df = pd.DataFrame()   # Additional info
        self.avg_df = pd.DataFrame() 
        self.avg_delta_df = pd.DataFrame()

    def __repr__(self) -> str:
        if self.df is None:
            return "Stock(Empty)"
        try:
            ticker = self.df.index.get_level_values("ticker")[0]
            return f"Stock(ticker={ticker})"
        except Exception as e:
            return f"Stock(Invalid: {e})"
        
    def avg_approximation(self):

        if not self.df.empty:
         # Since Yahoo Finance doesn't provide volume-adjusted average price, we approximate it using available data.
            self.df['VWAP_Price'] = self.df[['Open', 'Close', 'High', 'Low']].sum(axis=1) / 4
            
            #volatility = (3High-Open-Close-Low)/2 +|(3Low)-open-close-High|/2
            #the approximated volatile range for the price is = avg_price ± volatility.
            self.df['Volatility'] = (3*self.df['High'] - (self.df['Low'] + self.df['Open'] + self.df['Close']))/2+abs(3*self.df['Low'] - (self.df['High'] + self.df['Open'] + self.df['Close']))/2
            self.df['Max_change'] = self.df['High'] - self.df['Low']
            self.df['Datetime'] = pd.to_datetime(self.df['Datetime'])
            self.df['Volume_delta'] = self.df['Volume'].pct_change()
            self.df['Volatility_range'] = list(
                zip(
                    self.df['VWAP_Price'] - self.df['Volatility'],
                    self.df['VWAP_Price'] + self.df['Volatility']
                )
            )
        #other_df stores percentage changes such as delta
            # Set the datetime as index (cleaner for time groupings)
            df_indexed = self.df.set_index('Datetime')

            # Group by 30min, but don’t let it auto-expand range
            grouped = df_indexed.groupby(pd.Grouper(freq='30min'))
        
            # Drop intervals that have no data (they show up as all-NaN rows)
            # Reset index back to column
            self.avg_df['avg_volatility'] = grouped['Volatility'].mean().dropna()
            self.avg_df['avg_volume'] = grouped['Volume'].mean()
            self.avg_df['avg_open'] = grouped['Open'].mean()
            self.avg_df['avg_close'] = grouped['Close'].mean()
            self.avg_df['avg_high'] = grouped['High'].mean()
            self.avg_df['avg_low'] = grouped['Low'].mean()
            self.avg_delta_df['avg_volatility_delta'] = self.avg_df['avg_volatility'].pct_change()
            self.avg_delta_df['avg_volume_delta'] = self.avg_df['avg_volume'].pct_change()
            

            volume_df = self.df.reset_index()[['Datetime', 'Volume']].sort_values('Datetime')
            avg_df = self.avg_df.reset_index()[['Datetime', 'avg_volume']].sort_values('Datetime')

            # Merge asof on 'Datetime'
            df_result = pd.merge_asof(volume_df, avg_df, on='Datetime', direction='backward')

            # Calculate ratio
            self.delta_df['relative_volume'] = df_result['Volume'] / df_result['avg_volume']

        else:
            print("DataFrame is empty")

    @classmethod
    def from_ticker(cls, ticker):
        
        df = data_loader.get_stock(ticker)
        obj = cls()

        #return none if df is empty
        if df is None or df.empty:
            return None
        
        obj.df = df
        obj.name = ticker
        return obj

    
    
def debugger(stk: Stock):
    print(stk.df.head(30))
    print(stk.delta_df.head(30))
    print(stk.avg_df.head(30))
    print(stk.avg_delta_df.head(30))