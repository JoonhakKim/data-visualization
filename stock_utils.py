#stock_utilis gets data from data_loader and stores/handles data



import re
import logging 

def parse_interval(interval):
    match = re.match(r"(\d+)([a-zA-Z]+)", interval)
    if match:
        number = int(match.group(1))
        unit = match.group(2)
        return number, unit
    else:
        error_msg = f"Invalid interval format: '{interval}'"
        logging.error(error_msg)   # Log error to file
        raise ValueError(error_msg)  # Raise an exception

class StockPrice:
    def __init__(self, price, time_interval, time_frame, average):
        self.price = price                      # e.g., a list of prices or a pandas Series
        self.time_interval = time_interval      # e.g., '1d', '1m'

        self.time_interval = 
        
        match = re.match(r"(\d+)([a-zA-Z]+)", interval)
        if match:
            number = int(match.group(1)) 
            unit = match.group(2)
            print(number, unit)
        else:


        self.time_frame = time_frame            # e.g., '7d', '1mo'
        self.average = average                  # e.g., 5 for 5-day moving average


        self.window_size = time 

    def calculate_moving_average(self):
        # Assuming self.price is a pandas Series
        return self.price.rolling(window=self.average).mean()

    def latest_price(self):
        return self.price.iloc[-1]

    def summary(self):
        return {
            "Interval": self.time_interval,
            "Time Frame": self.time_frame,
            "Latest Price": self.latest_price(),
            "MA": self.calculate_moving_average().iloc[-1]
        }


