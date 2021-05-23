from buy_stocks import *
from random import choice

def test_buy_stock():
    count = 0
    for i in range(5):
        ticker = choice(tickersymbols)
        price = 45.45
        amount = 10
        s = buy_stock(ticker, price, amount)
        count += 1
        assert len(s) == count
        assert len(list(s.values())[count-1]) == 5

def test_calc_all_dividends():
    div_sum = float(calc_all_dividends().split()[-1])
    if len(securities_acc) > 0:
        assert div_sum > 0
    elif len(securities_acc) == 0:
        assert div_sum == 0

def test_calc_dividends():
    for i in range(10):
        ticker = choice(tickersymbols)
        result = calc_dividends(ticker)
        for t in securities_acc:
            if ticker in securities_acc[t]:
                assert result[1] == 0
            else:
                assert result[1] > 0
