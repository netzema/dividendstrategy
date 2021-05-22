import pandas as pd
import yfinance as yf
from pathlib import Path


# reading file in
# pathlib for efficient use of file paths
data_path = Path()
file = data_path / "Stocks on Watchlist.xlsx"
df = pd.read_excel(file)
# All stocks with an * in their name are dividend aristrocates. These companies have been increasing their dividends for 25 years in a row.

#df = pd.read_excel (r'C:\Users\netzl\OneDrive\Dokumente\Studium\Informatics Krems\2nd semester\Programming 2\INF-SS21-ProgrammingII-main\Exercise2\Stocks on Watchlist.xlsx')
#print (df)

# set up securites account
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
        self.signal = None
        self.transactions = {}

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
        'transactions': self.transactions
        }

    def deleteTransaction(self, _id):
        if _id in self.transactions:
            self.transactions.pop(_id)
            del securities_acc[_id]
            return self.name, self.transactions
        else:
            print("Transaction for this stock does not exist.")

    def calc_dividends(self):
        div_sum = 0
        if len(self.transactions) > 0:
            for i, t in self.transactions.items():
                div_sum += t["number_of_shares"] * t["dividend per share"]
        return self.ticker, div_sum
