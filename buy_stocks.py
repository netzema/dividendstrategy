from Stock import *
import datetime
import uuid
from data import *

def buy_stock(ticker, price, amount):
    s = getStockByTicker(ticker)
    divpershare = s.info['lastDividendValue']
    date = datetime.date.today().__str__()
    _id = uuid.uuid4().int
    s.transactions[_id] = {"date": date, "price": float(price), "number_of_shares": float(amount), "dividend per share": float(divpershare)}
    securities_acc[_id] = {"stock": s.name, "date": date, "price": float(price), "number_of_shares": float(amount), "dividend per share": float(divpershare)}
    return s.transactions

def calc_all_dividends():
    div_sum = 0
    for s in stocks:
        if len(s.transactions) > 0:
            for i, t in s.transactions.items():
                div_sum += t["number_of_shares"] * t["dividend per share"]
    return f"Sum of all dividends: {div_sum}"



# buy_stock("ben", 42.231, 100)
# buy_stock("ben", 39.0012, 300)
# buy_stock("abbv", 111.642, 100)
# calc_dividends("ben")
# calc_dividends("abbv")
# calc_all_dividends()
