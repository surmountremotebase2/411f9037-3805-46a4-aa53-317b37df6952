from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self, ticker="SPY"):
        self.ticker = ticker

    @property
    def assets(self):
        return [self.ticker]

    @property
    def interval(self):
        return "1day"

    def run(self, data):
        # Define the stake for holding, initialize to hold position (not buying or selling)
        stake = 0
        
        # Calculate the 50-day Simple Moving Average (SMA)
        sma50 = SMA(self.ticker, data["ohlcv"], 50)
        
        if len(sma50) > 2:  # Ensure we have at least three points to check direction
            # Check if SMA50 has reversed direction upwards by comparing the last three points
            if sma50[-2] < sma50[-1] and sma50[-3] > sma50[-2]:
                log(f"SMA50 has reversed direction upwards for {self.ticker}; entering buy trade.")
                stake = 1  # Set stake to 1 to indicate buying
                
            # Check if SMA50 has reversed direction downwards by comparing the last three points
            elif sma50[-2] > sma50[-1] and sma50[-3] < sma50[-2]:
                log(f"SMA50 has reversed direction downwards for {self.ticker}; entering sell trade.")
                stake = -1  # Set stake to -1 to indicate selling

        # Return a TargetAllocation with the calculated stake for the ticker
        return TargetAllocation({self.ticker: stake})