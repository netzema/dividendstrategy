from calculations import *
from random import sample, randint

# for testing we consider some random stocks and some random fng to avoid bias
def test_evaluate():
    n = 5
    tickers = sample(tickersymbols, n)
    for i in range(n):
        ticker = tickers[i]
        fng = randint(0,100)
        evaluate(ticker, fng)
        stock = getStockByTicker(ticker)
        # assert that signal has changed
        assert stock.signal in ["buy", "wait"]

def test_future_yield():
    n = 5
    tickers = sample(tickersymbols, n)
    for i in range(n):
        ticker = tickers[i]
        fng = randint(0, 100)
        date = "2025-04-30" # some random date
        result = future_yield(ticker, fng, date)
        # assert we get our two expected values
        assert len(result) == 2

def test_getGrahamNumber():
    n = 5
    tickers = sample(tickersymbols, n)
    for i in range(n):
        ticker = tickers[i]
        fng = randint(0, 100)
        result = getGrahamNumber(ticker, fng)
        # assert that all the results are calculated
        assert all(result)
        # assert that we get all the results we want
        assert len(result) == 5

# calculate_watchlist is just a mapping of the evaluate() function, thus no further testing needed
# future_calculation_of_stocks is just a mapping of the future_yield() function, thus no further testing needed

def test_calculate_watchlist():
    calculate_watchlist()
    # assert that every signal changed to either 'buy' or 'wait'
    assert all([s.signal in ["buy", "wait"] for s in stocks])

def test_future_calculation_of_stocks():
    date = "2025-04-30" # some random date
    fng, result = future_calculation_of_stocks(date)
    # assert that we get a result for every tracked stock
    assert len(result) == len(stocks)

def test_calculate_threshold():
    n = 5
    tickers = sample(tickersymbols, n)
    for i in range(n):
        ticker = tickers[i]
        result = calculate_threshold(ticker)
        # assert we get all the results needed
        assert len(result) == 4
        # assert that each result has some value
        assert all(result)
