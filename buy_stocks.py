from Stock import *
import datetime
import uuid
from data import *

# function to add a transaction of a stock to securities_acc
def buy_stock(ticker, price, amount):
    s = getStockByTicker(ticker)
    divpershare = s.info['lastDividendValue']  # store dividend per share
    if divpershare is None:
        divpershare = s.divyield * s.info["ask"]
    date = datetime.date.today().__str__() # get date
    _id = uuid.uuid4().int # construct unique id
    # add transaction to securities account
    securities_acc[_id] = {"stock": s.name, "date": date, "price": float(price), "number_of_shares": float(amount),
                           "dividend per share": float(divpershare)}
    return securities_acc

# function to calculate the sum of all dividends one would receive in a year
def calc_all_dividends():
    div_sum = 0
    # loop through transactions
    for t in securities_acc:
        trans = securities_acc[t] # access transaction by id
        # multiply number of shares by dividend per share
        div_sum += trans["number_of_shares"] * trans["dividend per share"]
    return f"Sum of all dividends: {round(div_sum,2)}"

# calculate dividends paid by one given company
def calc_dividends(ticker):
    div_sum = 0
    s = getStockByTicker(ticker)
    for t in securities_acc:
        trans = securities_acc[t]
        if trans["stock"] == s.name: # check if the name is the same
            div_sum += trans["number_of_shares"] * trans["dividend per share"]
    return ticker, round(div_sum,2)
