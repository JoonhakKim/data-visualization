import pandas as pd

from . import data_loader


class Stock:
    def __init__(self):
        #self.df must be panda dataframe. 
        #Otherwise everything would fall down, crumble and despair T_T
        self.df = pd.DataFrame()         # Main stock data
        self.percentage_df = pd.DataFrame()   # percentage info
        self.avg_df = pd.DataFrame()     
        self.avg_percentage_df = pd.DataFrame()
        self.name : str = ""
        #
    def __repr__(self) -> str:

        if self.df is None:
            return "Stock(Empty)"
        #try:
        ticker = self.df.index.get_level_values("ticker")[0]
        return f"Stock(ticker={ticker})"
        #except Exception as e:
            #return f"ERROR: {e})"
        
    def avg_approximation(self):

        if not self.df.empty:
            self.df.reset_index(level = 'ticker', drop = True, inplace =True) #inplace=True updates the DataFram instead of returning a new one
            print(f"index is :{self.df.index}")
         # Since Yahoo Finance doesn't provide volume-adjusted average price, we approximate it using available data.
            self.df['VWAP_Price'] = self.df[['Open', 'Close', 'High', 'Low']].sum(axis=1) / 4
            
            #volatility = (3High-Open-Close-Low)/2 +|(3Low)-Open-Close-High|/2
            #the approximated volatile range for the price is = avg_price ± volatility.
            self.df['Volatility'] = ((3*self.df['High'] - (self.df['Low'] + self.df['Open'] + self.df['Close']))
                                     /2+abs(3*self.df['Low'] - (self.df['High'] + self.df['Open'] + self.df['Close']))/2)
            self.df['Max_change'] = self.df['High'] - self.df['Low']
            self.df['Volume_delta'] = self.df['Volume'].pct_change()

            # a pair of min and max volatility
            self.df['Volatility_range'] = list(
                zip(
                    self.df['VWAP_Price'] - self.df['Volatility'],
                    self.df['VWAP_Price'] + self.df['Volatility']
                )
            )
        #other_df stores percentage changes such as delta
            # Set the datetime as index
            # Group by 30min
            b= self.df.resample('30min')
            print(b)
            grouped = self.df.groupby(pd.Grouper(freq = '30min'))
    
            self.avg_df['avg_volatility'] = grouped['Volatility'].mean().dropna()
            self.avg_df['avg_volume'] = grouped['Volume'].mean()
            self.avg_df['avg_open'] = grouped['Open'].mean()
            self.avg_df['avg_close'] = grouped['Close'].mean()
            self.avg_df['avg_high'] = grouped['High'].mean()
            self.avg_df['avg_low'] = grouped['Low'].mean()

        else:
            print("DataFrame is empty")


    #Enables building the Stock object without referencing .df everytime I create it. 
    #just a convinence function cuz I like the way c++ does constructing soooo
    @classmethod 
    def from_ticker(cls, ticker):
        
        df = data_loader.get_stock_from_yf(ticker)
        obj = cls()
        #return none if df is empty
        #none => no df object at all.
        #empty => df exist but has 0 rows (how empty is defined in pandas)
        if df is None or df.empty:
            return None
        
        obj.df = df
        obj.name = ticker
        return obj
    
    @classmethod 
    def db_from_ticker(cls, ticker):
        df = data_loader.load_stock_from_db(ticker)
        obj = cls()

        print(f"ticker is {ticker}")
        #return none if df is empty
        if df is None or df.empty:
            return None
        
        obj.df = df
        obj.name = ticker
        return obj

    



    
def debugger(stk: Stock):
    print(stk.df.head(30))
    print(stk.percentage_df.head(30))
    print(stk.avg_df.head(30))
    print(stk.percentage_df.head(30))




    '''
    def probability()

    np.mean(data)
    np.std(data)
    
    volatile range mean 
    volatile mean adjusted by the volume 
    
    
    
    
    '''