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
        self.signal = "To be determined" # will be determined by calculation, must be updated regularly
        self.currentDiv = None
        self.lastDiv = None
        self.divGrowth = "To be determined"
        self.five_year_avg_growth = "To be determined"
        self.growths = "To be determined"
        self.continuity = "To be determined"

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
        'signal': self.signal,
        'current dividend': self.currentDiv,
        'previous dividend': self.lastDiv,
        'dividend growth': self.divGrowth,
        'five year average growth': self.five_year_avg_growth,
        'Five year dividend growths': self.growths
        }

    def calcDivGrowth(self):
        try:
            divs = self.actions["Dividends"]["2015":"2021"]
            self.currentDiv = float(sum(divs["2020"]))
            self.lastDiv = float(sum(divs["2019"]))

            if isinstance(self.currentDiv, float) and isinstance(self.lastDiv, float):
                self.divGrowth = (self.currentDiv - self.lastDiv) * 100 /  self.lastDiv
            else:
                self.divGrowth = 0
            dividends_five_years = self.actions["2015":"2020"]["Dividends"]
            #divsum = sum(dividends_five_years)
            #len_divs = len(dividends_five_years)
            #five_year_average = divsum / len_divs
            growths = []
            growths.append(
                (sum(dividends_five_years["2016"]) - sum(dividends_five_years["2015"])) * 100 / sum(dividends_five_years["2015"]))
            growths.append(
                (sum(dividends_five_years["2017"]) - sum(dividends_five_years["2016"])) * 100 / sum(dividends_five_years["2016"]))
            growths.append(
                (sum(dividends_five_years["2018"]) - sum(dividends_five_years["2017"])) * 100 / sum(dividends_five_years["2017"]))
            growths.append(
                (sum(dividends_five_years["2019"]) - sum(dividends_five_years["2018"])) * 100 / sum(dividends_five_years["2018"]))
            growths.append(
                (sum(dividends_five_years["2020"]) - sum(dividends_five_years["2019"])) * 100 / sum(dividends_five_years["2019"]))
            self.growths = growths
            five_year_avg_growth = sum(growths) / len(growths)
            self.five_year_avg_growth = five_year_avg_growth
            self.continuity = all([False if d < 0 else True for d in self.growths])
            print(f"Success for {self.name}")
        except Exception as e:
            print(e, type(e).__name__)
            print(f"No response for {self.name}")
            self.five_year_avg_growth = 0
            self.growths = []
            self.currentDiv = 0
            self.lastDiv = 0
            self.divGrowth = 0