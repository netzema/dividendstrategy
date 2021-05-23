from Dividend_Strategy_API import *
from random import choice

# for testing we consider some random stocks and some random fng
def test_getWL():
    with app.app_context():
        result = getWL()
        assert result.status_code == 200

def test_fng():
    with app.app_context():
        result = fng()
        assert result.status_code == 200

def test_getTicker():
    with app.app_context():
        ticker = choice(tickersymbols)
        result = getTicker(ticker)
        assert result.status_code == 200

def test_prices():
    with app.app_context():
        ticker = choice(tickersymbols)
        result = prices(ticker)
        assert result.status_code == 200

def test_calulations():
    with app.app_context():
        result = calulations()
        assert result.status_code == 200

def test_future_calculations():
    with app.app_context():
        date = "2022-04-30"
        result = future_calculations(date)
        assert result.status_code == 200

def test_getBuy():
    with app.app_context():
        result = getBuy()
        assert result.status_code == 200

def test_getSignal():
    with app.app_context():
        ticker = choice(tickersymbols)
        result = getSignal(ticker)
        assert result.status_code == 200

def test_getThreshold():
    with app.app_context():
        ticker = choice(tickersymbols)
        result = getThreshold(ticker)
        assert result.status_code == 200

def test_buyStock():
    with app.app_context():
        ticker = choice(tickersymbols)
        price = 45.45
        amount = 10
        result = buyStock(ticker, price, amount)
        assert result.status_code == 200

def test_getDivs():
    with app.app_context():
        ticker = choice(tickersymbols)
        result = getDivs(ticker)
        assert result.status_code == 200

def test_getAllDivs():
    with app.app_context():
        result = getAllDivs()
        assert result.status_code == 200

def test_delTrans():
    with app.app_context():
        securities_acc[478903479358734] = {"stock": "TestStock", "date": "2020-05-23", "price": 45.45,
                                            "number_of_shares": 10, "dividend per share": 0.59}
        k = 478903479358734
        result = delTrans(k)
        assert result == {}

def test_getAllTransactions():
    with app.app_context():
        result = getAllTransactions()
        assert result.status_code == 200

def test_graham():
    with app.app_context():
        results = []
        for i in range(5):
            ticker = choice(tickersymbols)
            result = graham(ticker)
            results.append(len(result) == 5 and all(result))
        assert all(results)

# all functions are tested and working!
