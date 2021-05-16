import datetime
from Stock import *


### custom evaluation
# get stock price progress within the year before covid outbreak
# yield that progress to now and get the value
# also consider current market mood

def evaluate(ticker, fng):
    try:
        # get prices from a year before covid breakout
        preCovid = yf.download(ticker, start = "2019-02-01", end = "2020-02-1") # fetch data from yahoo finance
        stock = getStockByTicker(ticker) # Stock instance

        base = preCovid.iloc[0]["High"] # store the price at the beginnig of the mentioned perio
        breakout = preCovid.iloc[-1]["High"] # store the last value before the crash
        step = (breakout - base) / base # calculate the factor in percent of the price development
        current = yf.download(ticker, period = "1d") # get current data of the stock
        d = datetime.date.today() - datetime.date(2020,2,1,) # calculate the difference in days between breakout and now
        days = int(d.__str__().split()[0]) # convert datetimes days to integer

        calcPrice = breakout*(1+(step/365*days)) # calculate the price if the trend had not left off
        currentPrice = current.iloc[-1]["High"] # store current price

        # the higher the fng the worse time it is to buy stocks, thus we caluclated an fng adjusted price
        # at this price we would consider to buy a stock
        if fng > 75:
            adjustedPrice = calcPrice * 2
        elif fng > 50:
            adjustedPrice = calcPrice * 1.5
        elif fng > 25:
            adjustedPrice = calcPrice
        else:
            adjustedPrice = calcPrice * 0.75

        if currentPrice < adjustedPrice:
            stock.signal = "buy" # emit a buy signal if adjusted price is higher than current price
        else:
            stock.signal = "wait"

        return round(adjustedPrice,2), round(currentPrice,2)
    except:
        # on some days some information might still be missing on the api
        print(f"Currently no evaluation possible for {ticker}.")

# for stock in stocks:
#     evaluate(stock.ticker, 40)
#     print(f"Evaluating Stock #{stocks.index(stock)} from {len(stocks)}...")



# tickers = yf.Tickers([t.ticker for t in stocks[0:10]])
# dat = yf.download(" ".join([t.ticker for t in stocks]), period = "1d")



### get graham number
#ticker = "MSFT"
#stock = list(filter(lambda x: x.ticker == ticker, stocks))[0]
#stock.info["trailingEps"]
#stock.info["bookValue"]
#stock.info["priceToBook"]

def getGrahamNumber(ticker, fng):
    stock = getStockByTicker(ticker)
    info = stock.info
    try:
        eps = info["trailingEps"] if "trailingEps" in info else info["forwardEps"]
        bookValue = info["bookValue"]
    except:
        return f"No evaluation possible for {ticker}"
    try:
        graham = round((22.5 * eps * bookValue)**0.5, 2)
    except TypeError:
        stock.signal = "wait"
        return f"No evalution possible for {ticker} at the moment"

    if 'ask' in info and info['ask'] > 0:
        currentPrice = info['ask']
    elif 'bid' in info and info['bid'] > 0:
        currentPrice = info['bid']
    elif 'dayHigh' in info and info['dayHigh'] > 0:
        currentPrice = info['dayHigh']
    if fng > 75:
        adjustedPrice = currentPrice*2
    elif fng > 50:
        adjustedPrice = currentPrice*1.5
    elif fng > 25:
        adjustedPrice = currentPrice
    else:
        adjustedPrice = currentPrice * 0.75

    if adjustedPrice < graham:
        stock.signal = "buy"
    else:
        stock.signal = "wait"

    return {"ticker": ticker,
            "signal": stock.signal,
            "Fair value": graham,
            "Adjusted value": adjustedPrice,
            "Current value": currentPrice
            }