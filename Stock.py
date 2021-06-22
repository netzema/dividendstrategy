import wbdata
from os import path
import pickle
from data import *

# store all stocks in a list accessing the read in pandas dataframe
stocks = [Stock(df['Name'][i],
                str(df['Ticker'][i]),
                df['ISIN'][i],
                float(df['Div. Yield'][i][:-1]),
                df['Branche'][i],
                df['Country'][i],
                int(df['Frequency'][i][-1])) for i in range(len(df))]

# filter countries with high withholding tax
stocks = [s for s in stocks if s.country not in ["DE1", "FR1", "CH1"]]
def filter_Stocks(stockslist):
    # only evaluate stocks where
    # - the dividend growth is higher than the current inflation rate
    # - the five year average dividend growth if higher than the current inflation rate
    # - and there has been a dividend continuity of at least 5 years
    rate_current = wbdata.get_data("FP.CPI.TOTL.ZG", country="AUT")[0]["value"]  # store inflation rate
    rate_lastyear = wbdata.get_data("FP.CPI.TOTL.ZG", country="AUT")[1]["value"]  # store last year's rate
    inflation_rate = rate_current if rate_current is not None else rate_lastyear  # in case this year's has not been released
    [stock.calcDivGrowth() for stock in stockslist]
    watchlist = list(filter(lambda x: x.divGrowth and x.five_year_avg_growth and x.divGrowth >= inflation_rate and x.five_year_avg_growth >= inflation_rate
                       and x.continuity, stockslist))
    return watchlist

# store all ticker symbols in a list
tickersymbols = [s.ticker for s in stocks]


# function to get a stock knowing its ticker
def getStockByTicker(tickersymbol):
    tickersymbol = tickersymbol.upper()
    if tickersymbol in tickersymbols:
        # gets a list of all stocks with given ticker symbol, but ticker symbol is unique for every stock
        # so we get list of len = 1 and access the first element
        return list(filter(lambda x: x.ticker == tickersymbol, stocks))[0]
    else:
        return "Ticker not found."

def getStockInfo(tickersymbol):
    stock = getStockByTicker(tickersymbol)
    if stock is not None:
        info = stock.info
        return {"name": stock.name,
            "ticker": stock.ticker,
            "ISIN": stock.ISIN,
            "Dividend Yield": stock.divyield,
            "branch": stock.branch,
            "country": stock.country,
            "payout frequency": stock.frequency,
            "signal": stock.signal,
            "dividend per share": info['lastDividendValue'] if info['lastDividendValue'] is not None else info['ask'] * (stock.divyield/100),
            "52-week high": info['fiftyTwoWeekHigh'] if 'fiftyTwoWeekHigh' in info else None,
            "52-week low": info['fiftyTwoWeekLow'] if 'fiftyTwoWeekLow' in info else None,
            "ask price": info['ask'] if 'ask' in info else None,
            "bid price": info['bid'] if 'bid' in info else None,
            "day high": info['dayHigh'] if 'dayHigh' in info else None
            }
    else:
        return "ERROR: Please enter a valid ticker symbol."

def getPrice(tickersymbol):
    stock = getStockByTicker(tickersymbol)
    if stock != None:
        info = stock.info
        return {"name": stock.name,
                "ticker": stock.ticker,
                "ask price": info['ask'] if 'ask' in info else None,
                "bid price": info['bid'] if 'bid' in info else None,
                "day high": info['dayHigh'] if 'dayHigh' in info else None}
    else:
        return "ERROR: Please enter a valid ticker symbol."
