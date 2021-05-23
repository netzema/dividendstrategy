from Stock import *
from random import choice


def test_getStockByTicker():
    for i in range(10):
        ticker = choice(tickersymbols)
        stock = getStockByTicker(ticker)
        assert stock.ticker == ticker

def test_inflationrate():
    rate_current = wbdata.get_data("FP.CPI.TOTL.ZG", country="AUT")[0]["value"]
    rate_lastyear = wbdata.get_data("FP.CPI.TOTL.ZG", country="AUT")[1]["value"]
    inflation_rate = rate_current if rate_current is not None else rate_lastyear
    assert inflation_rate is not None
    assert 0 < inflation_rate < 7

def test_getStockInfo():
    for i in range(5):
        ticker = choice(tickersymbols)
        result = getStockInfo(ticker)
        assert len(result) == 14
        assert all(list(result.values()))

def test_getPrice():
    for i in range(5):
        ticker = choice(tickersymbols)
        result = getPrice(ticker)
        assert len(result) == 5
        assert all(list(result.values()))

