import pandas as pd
import yfinance as yf
from pathlib import Path


# reading file in
# pathlib for efficient use of file paths
data_path = Path()
file = data_path / "Stocks on Watchlist.xlsx"
df = pd.read_excel(file)
# All stocks with an * in their name are dividend aristrocates.
# These companies have been increasing their dividends for 25 years in a row.

# set up securities account
# transactions are stored within it
# it interacts with the database file
securities_acc = {}

# define Stock class inheriting yf.Ticker
class Stock(yf.Ticker):
    def __init__(self, name, ticker, ISIN, divyield, branch, country, frequency):
        yf.Ticker.__init__(self, ticker)
        self.name = name
        self.ticker = ticker
        self.ISIN = ISIN
        self.divyield = divyield
        self.branch = branch
        self.country = country
        self.frequency = frequency
        self.signal = None # will be determined by calculation, must be updated regularly

    def __repr__(self):
        return self.name

    def serialize(self):
        return {
        'name': self.name,
        'ticker': self.ticker,
        'ISIN': self.ISIN,
        'dividend yield': self.divyield,
        'branch': self.branch,
        'country': self.country,
        'frequency': self.frequency,
        'signal': self.signal
        }