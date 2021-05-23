import datetime
from Stock import *
import fear_and_greed
from time import sleep


### custom evaluation ###
# get stock price progress within the year before covid outbreak
# yield that progress to now and get the value
# also consider current market mood

def evaluate(ticker, fng):
    try:
        # get prices from a year before covid breakout
        preCovid = yf.download(ticker, start = "2019-02-01", end = "2020-02-1") # fetch data from yahoo finance
        stock = getStockByTicker(ticker) # Stock instance

        base = preCovid.iloc[0]["High"] # store the price at the beginning of the pre-covid period
        breakout = preCovid.iloc[-1]["High"] # store the last value before the crash
        step = (breakout - base) / base # calculate the price development in percent
        current = yf.download(ticker, period = "1d") # get current data of the stock
        d = datetime.date.today() - datetime.date(2020,2,1,) # calculate the difference in days between breakout and now
        days = int(d.__str__().split()[0]) # convert datetime days to integer

        calcPrice = breakout*(1+(step/365*days)) # calculate the price if the trend had not let off
        ### the step equals the price development within one year before the outbrake
        ### the step is than mapped to the number of days since the breakout
        ### convert to a factor and multiply the last price before the breakout with the new step factor
        currentPrice = current.iloc[-1]["High"] # store current price

        # the higher the fear-and-greed index (fng) the worse time it is to buy stocks,
        # thus we calculate an fng adjusted price
        # at this price we would consider buying the stock
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
        return (0,0)

def future_yield(ticker, fng, date):
    # map the calculation schema to any point in the future (necessarily post breakout)
    try:
        # get prices from a year before covid breakout
        preCovid = yf.download(ticker, start = "2019-02-01", end = "2020-02-1") # fetch data from yahoo finance

        base = preCovid.iloc[0]["High"] # store the price at the beginning of the mentioned period
        breakout = preCovid.iloc[-1]["High"] # store the last value before the crash
        step = (breakout - base) / base # calculate the factor in percent of the price development
        date = date.split("-")
        year, month, day = int(date[0]), int(date[1]), int(date[2]) # store date as three integers
        days = datetime.date.today() - datetime.date(year, month, day) # calculate the difference in days between
        # breakout and the given date
        days = int(days.__str__().split()[0]) # convert datetime days to integer

        calcPrice = breakout*(1+(step/365*days)) # calculate the price if the trend had not let off

        # the higher the fng the worse time it is to buy stocks, thus we calculated an fng adjusted price
        # at this price we would consider to buy a stock
        if fng > 75:
            adjustedPrice = calcPrice * 2
        elif fng > 50:
            adjustedPrice = calcPrice * 1.5
        elif fng > 25:
            adjustedPrice = calcPrice
        else:
            adjustedPrice = calcPrice * 0.75
        return (ticker, adjustedPrice)
    except:
        # on some days some information might still be missing on the api
        print(f"Currently no evaluation possible for {ticker}.")
        return (ticker, 0)

# the next function is some additional method to evaluate stocks, which is not made up by myself
# it is just a little extra, but not needed for the project itself.
def getGrahamNumber(ticker, fng):
    stock = getStockByTicker(ticker)
    info = stock.info # get all the information of the stock
    try:
        # get earnings per share (eps) and the bookvalue
        eps = info["trailingEps"] if "trailingEps" in info else info["forwardEps"]
        bookValue = info["bookValue"]
    except:
        return f"No evaluation possible for {ticker}"
    try:
        graham = round((22.5 * eps * bookValue)**0.5, 2) # formula for the graham number
    except TypeError: # not every dataset is consistent, some may have different entries or none at all
        stock.signal = "wait"
        return f"No evaluation possible for {ticker} at the moment"

    # get current price of the stock
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

def calculate_watchlist():
    fng = list(fear_and_greed.get())
    print("Now fetching data of all stocks... This might take a while. Grab a cup of coffee in the meantime.")
    sleep(1)
    for stock in stocks:
        evaluate(stock.ticker, fng[0])
        print(f"Evaluating Stock #{stocks.index(stock)} from {len(stocks)-1}...")

def future_calculation_of_stocks(date):
    fng = list(fear_and_greed.get())
    print("Now fetching data of all stocks... This might take a while. Grab a cup of coffee in the meantime.")
    sleep(1)
    result = []
    for stock in stocks:
        result.append(future_yield(stock.ticker, fng[0], date))
        print(f"Evaluating Stock #{stocks.index(stock)} from {len(stocks)}...")
    return fng, result

def calculate_threshold(tickersymbol):
    stock = getStockByTicker(tickersymbol)
    prices = evaluate(tickersymbol, list(fear_and_greed.get())[0])
    if prices[0] > prices[1]:
        stock.signal = "buy"
    else:
        stock.signal = "wait"
    return stock.name, stock.ticker, prices[0], prices[1]