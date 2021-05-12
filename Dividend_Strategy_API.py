from flask import Flask, request, jsonify
from Stock import *

import fear_and_greed

app = Flask(__name__)

#get watchlist
@app.route("/wl", methods=["GET"])
def getWL():
    return jsonify(fear_and_greed_index=list(fear_and_greed.get()),
                   watchlist=[stock.serialize() for stock in stocks])

#get list of all stocks which emit a buy signal
@app.route("/buy", methods=["GET"])
def getBuy():
    return jsonify([stock.name for stock in stocks if stock.signal == "buy"])

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
    response.headers['Access-Control-Allow-Methods']=  "POST, GET, PUT, DELETE"
    return response

if __name__ == "__main__":
    app.run(debug=True, port=8888)

