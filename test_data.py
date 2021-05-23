from data import *
from Stock import *
from random import choice

def test_serialize():
    for i in range(10):
        stock = choice(stocks)
        out = stock.serialize()
        assert list(out.keys()) == ['name','ticker','ISIN','dividend yield','branch','country','frequency', 'signal']
        assert list(out.values()) == [stock.name,stock.ticker,stock.ISIN,stock.divyield,stock.branch,stock.country,stock.frequency,stock.signal]

def test_df():
    assert len(df) == 409
    assert ('Name' and 'Branche' and 'Country' and 'ISIN' and 'Frequency' and 'Div. Yield' and 'Links' and 'Ticker') in list(df.columns)

