from data import *

# store all stocks in a list
stocks = [Stock(df['Name'][i], str(df['Ticker'][i]), df['ISIN'][i], float(df['Div. Yield'][i][:-1]), df['Branche'][i], df['Country'][i], int(df['Frequency'][i][-1])) for i in range(len(df))]

# filter counties with high withholding tax
stocks = [s for s in stocks if s.country not in ["DE1", "FR1", "CH1"]]

# store all tickersymbols for error handling
tickersymbols = [s.ticker for s in stocks]

# function to get a stock knowing its ticker
def getStockByTicker(tickersymbol):
    tickersymbol = tickersymbol.upper()
    if tickersymbol in tickersymbols:
        return list(filter(lambda x: x.ticker == tickersymbol, stocks))[0]
    else: return None

#print(stocks)

# get info of certain stock knowing its ticker
#ticker = "MSFT"
#stock = list(filter(lambda x: x.ticker == ticker, stocks))[0]
#stock.info

# get dividend payed out per share
#stock.info['lastDividendValue']

# 52-week high
#stock.info['fiftyTwoWeekHigh']

# 52-week low
#stock.info['fiftyTwoWeekLow']

# # get historical market data
#hist = stock.history(period="max")

# get open, high, low etc from certain date
#hist.query("Date == '2019-05-08'")
# get open, high, low etc from certain time period
#hist.query("'2018-05-08' <= Date <= '2019-05-08'")

# extract the price of that period
#hist.query("Date == '2019-05-08'")['High']
#hist.query("'2018-05-08' <= Date <= '2019-05-08'")['High']

### other useful methods ###

# # show actions (dividends, splits)
# stocks[0].actions
#
# # show dividends
# stocks[0].dividends
#
# # show splits
# stocks[0].splits
#
# # show financials
# stocks[0].financials
# stocks[0].quarterly_financials
#
# # show major holders
# stocks[0].major_holders
#
# # show institutional holders
# stocks[0].institutional_holders
#
# # show balance sheet
# stocks[0].balance_sheet
# stocks[0].quarterly_balance_sheet
#
# # show cashflow
# stocks[0].cashflow
# stocks[0].quarterly_cashflow
#
# # show earnings
# stocks[0].earnings
# stocks[0].quarterly_earnings
#
# # show sustainability
# stocks[0].sustainability
#
# # show analysts recommendations
# stocks[0].recommendations
#
# # show next event (earnings, etc)
# stocks[0].calendar
#
# # show ISIN code - *experimental*
# # ISIN = International Securities Identification Number
# stocks[0].isin
#
# # show options expirations
# stocks[0].options