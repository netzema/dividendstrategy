from Dividend_Strategy_API import *
from Stock import *

def test_getWL():
    output = [stock.serialize() for stock in stocks]
    assert [o["name"] for o in output] == [s.name for s in stocks]

