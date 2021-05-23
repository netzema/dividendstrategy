from calculations import *
from random import choice, randint

# for testing we consider some random stocks and some random fng
def test_evaluate():
    ticker = choice(tickersymbols)
    fng = randint(0,100)
    evaluate(ticker, fng)
    stock = getStockByTicker(ticker)
    assert stock.signal in ["buy", "wait"]

def test_future_yield():
    ticker = choice(tickersymbols)
    fng = randint(0, 100)
    date = "2025-04-30"
    result = future_yield(ticker, fng, date)
    assert len(result) == 2

def test_getGrahamNumber():
    ticker = choice(tickersymbols)
    fng = randint(0, 100)
    result = getGrahamNumber(ticker, fng)
    assert all(result)
    assert len(result) == 5

# calculate_watchlist is just a mapping of the evaluate() function, thus no further testing needed
# future_calculation_of_stocks is just a mapping of the future_yield() function, thus no further testing needed

def test_calculate_watchlist():
    calculate_watchlist()
    assert all([s.signal in ["buy", "wait"] for s in stocks])

def test_future_calculation_of_stocks():
    date = "2025-04-30"
    fng, result = future_calculation_of_stocks(date)
    assert len(result) == len(stocks)

def test_calculate_threshold():
    ticker = choice(tickersymbols)
    result = calculate_threshold(ticker)
    assert len(result) == 4
    assert all(result)
