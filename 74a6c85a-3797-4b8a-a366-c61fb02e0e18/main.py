from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log
from surmount.data import OHLCVData

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["AAPL"]  # Use any ticker(s) you want to trade

    @property
    def interval(self):
        return "15min"  # Set the time frame to 15 minutes

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return [OHLCVData(i) for i in self.tickers]  # OHLCV data for the tickers

    def run(self, data):
        allocation = {}
        for ticker in self.tickers:
            # Fetch the 50 and 200 period SMA for the ticker
            sma50 = SMA(ticker, data["ohlcv"], 50)
            sma200 = SMA(ticker, data["ohlcv"], 200)

            if len(sma50) < 2 or len(sma200) < 2:
                # Not enough data to decide
                continue

            # Determine whether the curves have reached minima or maxima
            minima_sma50 = sma50[-2] > sma50[-1] < sma50[-3]
            minima_sma200 = sma200[-2] > sma200[-1] < sma200[-3]
            maxima_sma50 = sma50[-2] < sma50[-1] > sma50[-3]
            maxima_sma200 = sma200[-2] < sma200[-1] > sma200[-3]

            # Allocate based on maxima and minima conditions
            if minima_sma50 and minima_sma200:
                # Both MA curves reaching minima and about to move upwards: Buy signal
                allocation[ticker] = 1.0
                log(f"Buying {ticker} as both 50 and 200 MA curves are at their respective minima.")
            elif maxima_sma50 and maxima_sma200:
                # Both MA curves reaching maxima and about to move downwards: Sell signal (shorting)
                allocation[ticker] = -1.0  # Assuming short selling is allowed, change accordingly
                log(f"Selling {ticker} as both 50 and 200 MA curves are at their respective maxima.")
            else:
                # No clear signal, do not hold position
                allocation[ticker] = 0
                log(f"No clear trade signal for {ticker}.")

        return TargetAllocation(allocation)