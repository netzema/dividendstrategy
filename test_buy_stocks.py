from buy_stocks import *
from random import choice, sample

def test_calc_all_dividends():
    # assert that we do not get dividends if we do not own stocks
    # returns a string, we split it and take only the calculated dividends
    div_sum = float(calc_all_dividends().split()[-1])
    assert div_sum == 0
    # buy a stock and assert we now receive dividends
    buy_stock(choice(tickersymbols), 45.45, 10)
    div_sum = float(calc_all_dividends().split()[-1])
    assert div_sum > 0

def test_buy_stock():
    count = len(securities_acc)
    n = 5
    tickers = sample(tickersymbols, n)
    for i in range(n):
        ticker = tickers[i]
        price = 45.45
        amount = 10
        s = buy_stock(ticker, price, amount) # returns securities_acc, each loop adds one transaction
        count += 1
        # assert that all transactions are in securities_acc
        assert len(s) == count
        # assert we have all the necessary values, accessing index of the transactions
        assert len(list(s.values())[count-1]) == 5

def test_calc_dividends():
    # test one stock which is already bought (and thus pays the user dividends) and one which is not
    securities_acc = {}
    tickers = sample(tickersymbols, 2)
    ticker1 = tickers[0]
    ticker2 = tickers[1]
    s1 = getStockByTicker(ticker1)
    s2 = getStockByTicker(ticker2)
    # mark first stock as bought
    buy_stock(ticker1, 45.45, 10)
    result1 = calc_dividends(ticker1)
    result2 = calc_dividends(ticker2)
    # pays dividends
    assert result1[0] == s1.ticker and result1[1] > 0
    # does not pay dividends as stock is not bought
    assert result2[0] == s2.ticker and result2[1] == 0
