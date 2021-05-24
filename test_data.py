from data import *
from Stock import *
from random import sample

def test_serialize():
    n = 10
    s = sample(stocks, n)
    for i in range(n):
        stock = s[i]
        out = stock.serialize()
        # assert that all keys are obtained
        assert list(out.keys()) == ['name','ticker','ISIN','dividend yield','branch','country','frequency', 'signal']
        # assert that all values are obtained
        assert list(out.values()) == [stock.name,stock.ticker,stock.ISIN,stock.divyield,stock.branch,stock.country,stock.frequency,stock.signal]

def test_df():
    # assert we get all the relevant stocks
    assert len(df) == 409
    # assert we get all the necessary columns
    assert ('Name' and 'Branche' and 'Country' and 'ISIN' and 'Frequency' and 'Div. Yield' and 'Links' and 'Ticker') in list(df.columns)

