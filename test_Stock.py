from Stock import *
from random import choice


def test_getStockByTicker():
    for i in range(10):
        ticker = choice(tickersymbols)
        stock = getStockByTicker(ticker)
        assert stock.ticker == ticker

