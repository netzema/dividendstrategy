from Stock import *
from random import choice, sample

# to not get biased results, we test random stocks using choice on list of ticker symbols

def test_getStockByTicker():
    n = 10
    tickers = sample(tickersymbols, n)
    for i in range(n):
        ticker = tickers[i]
        stock = getStockByTicker(ticker)
        # assert that every stock pays dividends
        assert stock.ticker == ticker and stock.divyield > 0

def test_inflationrate():
    rate_current = wbdata.get_data("FP.CPI.TOTL.ZG", country="AUT")[0]["value"]
    rate_lastyear = wbdata.get_data("FP.CPI.TOTL.ZG", country="AUT")[1]["value"]
    inflation_rate = rate_current if rate_current is not None else rate_lastyear
    assert inflation_rate is not None
    assert 0 < inflation_rate < 10 # otherwise we would have other problems than this dividend tracking software...

def test_getStockInfo():
    n = 5
    tickers = sample(tickersymbols, n)
    for i in range(n):
        ticker = tickers[i]
        result = getStockInfo(ticker)
        # assert that we get all the necessary results
        assert len(result) == 14
        # assert that all the values are scraped / calculated
        assert all(list(result.values()))

def test_getPrice():
    n = 5
    tickers = sample(tickersymbols, n)
    for i in range(n):
        ticker = tickers[i]
        result = getPrice(ticker)
        # assert that we get all the necessary results
        assert len(result) == 5
        # assert that all the values are scraped / calculated
        assert all(list(result.values()))
