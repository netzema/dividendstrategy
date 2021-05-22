from time import sleep
import fear_and_greed
from flask import Flask, jsonify
from calculations import *
from Stock import *
from buy_stocks import *
from data import *

app = Flask(__name__)


#get watchlist
@app.route("/wl", methods=["GET"])
def getWL():
    return jsonify(fear_and_greed_index=list(fear_and_greed.get()),
                   watchlist=[stock.serialize() for stock in stocks])

#get fear and greed index
@app.route("/fng", methods=["GET"])
def fng():
    return jsonify(fear_and_greed_index=list(fear_and_greed.get()))

#get info of one specific stock knowing its ticker symbol
@app.route("/<tickersymbol>", methods=["GET"])
def getTicker(tickersymbol):
    stock = getStockByTicker(tickersymbol)
    if stock != None:
        info = stock.info
        return jsonify(stockinformation=[{"name": stock.name,
            "ticker": stock.ticker,
            "ISIN": stock.ISIN,
            "Dividend Yield": stock.divyield,
            "branch": stock.branch,
            "country": stock.country,
            "payout frequency": stock.frequency,
            "signal": stock.signal,
            "dividend per share": info['lastDividendValue'] if 'lastDividendValue' in info else None,
            "52-week high": info['fiftyTwoWeekHigh'] if 'fiftyTwoWeekHigh' in info else None,
            "52-week low": info['fiftyTwoWeekLow'] if 'fiftyTwoWeekLow' in info else None,
            "ask price": info['ask'] if 'ask' in info else None,
            "bid price": info['bid'] if 'bid' in info else None,
            "day high": info['dayHigh'] if 'dayHigh' in info else None
            }])
    else: return "ERROR: Please enter a valid ticker symbol."

#get price of one specific stock knowing its ticker symbol
@app.route("/<tickersymbol>/price", methods=["GET"])
def getPrice(tickersymbol):
    stock = getStockByTicker(tickersymbol)
    if stock != None:
        info = stock.info
        return jsonify(stockprice=[{"name": stock.name,
                                    "ticker": stock.ticker,
                                    "ask price": info['ask'] if 'ask' in info else None,
                                    "bid price": info['bid'] if 'bid' in info else None,
                                    "day high": info['dayHigh'] if 'dayHigh' in info else None}])
    else:
        return "ERROR: Please enter a valid ticker symbol."

#do evaluation and return edited watchlist
@app.route("/calc", methods=["GET"])
def calulations():
    fng = list(fear_and_greed.get())
    print("Now fetching data of all stocks... This might take a while. Grab a cup of coffee in the meantime.")
    sleep(1)
    for stock in stocks:
        evaluate(stock.ticker, fng[0])
        print(f"Evaluating Stock #{stocks.index(stock)} from {len(stocks)}...")
    return jsonify(fear_and_greed_index=fng,
                   watchlist=[stock.serialize() for stock in stocks])

#do evaluation
@app.route("/calc/<date>", methods=["GET"])
def future_calculations(date):
    fng = list(fear_and_greed.get())
    print("Now fetching data of all stocks... This might take a while. Grab a cup of coffee in the meantime.")
    sleep(1)
    result = []
    for stock in stocks:
        result.append(future_yield(stock.ticker, fng[0], date))
        print(f"Evaluating Stock #{stocks.index(stock)} from {len(stocks)}...")
    return jsonify(fear_and_greed_index=fng,
                   trend=result)

#get list of all stocks which emit a buy signal
@app.route("/buy", methods=["GET"])
def getBuy():
    return jsonify([stock.name for stock in stocks if stock.signal == "buy"])

#get a stocks' recommendation
@app.route("/<tickersymbol>/recommendation", methods=["GET"])
def getSignal(tickersymbol):
    stock = getStockByTicker(tickersymbol)
    return jsonify(Name=stock.name,
                   Ticker=stock.ticker,
                   Recommendation=stock.signal)

#get a stocks' threshold, below which I would consider to buy
@app.route("/<tickersymbol>/threshold", methods=["GET"])
def getThreshold(tickersymbol):
    stock = getStockByTicker(tickersymbol)
    prices = evaluate(tickersymbol, list(fear_and_greed.get())[0])
    if prices[0] > prices[1]:
        stock.signal = "buy"
    else:
        stock.signal = "wait"
    return jsonify(Name=stock.name,
                   Ticker=stock.ticker,
                   Threshold=prices[0],
                   CurrentPrice=prices[1])

#buy a stock (parameters: ticker symbol, price, amount
@app.route("/buy/<tickersymbol>/<price>/<amount>", methods=["POST"])
def buyStock(tickersymbol, price, amount):
    trans = buy_stock(tickersymbol, price, amount)
    return jsonify(transactions= trans)

#get the dividends received of a bought stock
@app.route("/<tickersymbol>/div", methods=["GET"])
def getDivs(tickersymbol):
    s = getStockByTicker(tickersymbol)
    return jsonify(s.calc_dividends())

#get all dividends which will be received this year
@app.route("/dividends", methods=["GET"])
def getAllDivs():
    return jsonify(calc_all_dividends())

#delete a transaction from the securities account
@app.route("/delete/<tickersymbol>/<int:transaction_id>", methods=["DELETE"])
def delTrans(tickersymbol, transaction_id):
    s = getStockByTicker(tickersymbol)
    s.deleteTransaction(transaction_id)
    return s.transactions

#display all transactions
@app.route("/transactions", methods=["GET"])
def getAllTransactions():
    return jsonify(transactions = securities_acc)

#######################
@app.route("/")
def index():
    return jsonify(
            success = True,
            message = "Your server is running! Welcome to the Daniel's dividend strategy API.")

@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] =  "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    response.headers['Access-Control-Allow-Methods']=  "POST, GET, PUT, DELETE, PATCH"
    return response

if __name__ == "__main__":
    app.run(debug=True, port=8888)

