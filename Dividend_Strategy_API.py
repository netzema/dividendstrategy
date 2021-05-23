from flask import Flask, jsonify

from buy_stocks import *
from calculations import *
from dbm import *

app = Flask(__name__)

#get watchlist, return fear and greed index information and every stock's information
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
    return jsonify(stockinformation= getStockInfo(tickersymbol))

#get price of one specific stock knowing its ticker symbol
@app.route("/<tickersymbol>/price", methods=["GET"])
def prices(tickersymbol):
    return jsonify(price = getPrice(tickersymbol))

#do evaluation and return edited watchlist
@app.route("/calc", methods=["GET"])
def calulations():
    fng = list(fear_and_greed.get())
    calculate_watchlist()
    return jsonify(fear_and_greed_index=fng,
                   watchlist=[stock.serialize() for stock in stocks])

#do evaluation
@app.route("/calc/<date>", methods=["GET"])
def future_calculations(date):
    fng, result = future_calculation_of_stocks(date)
    return jsonify(fng=fng, result=result)

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
    name, ticker, threshold, currentprice = calculate_threshold(tickersymbol)
    return jsonify(Name=name,
                   Ticker=ticker,
                   Threshold=threshold,
                   CurrentPrice=currentprice)

#buy a stock (parameters: ticker symbol, price, amount
@app.route("/buy/<tickersymbol>/<price>/<amount>", methods=["POST"])
def buyStock(tickersymbol, price, amount):
    trans = buy_stock(tickersymbol, price, amount)
    return jsonify(transactions= trans)

#get the dividends received of a bought stock
@app.route("/<tickersymbol>/div", methods=["GET"])
def getDivs(tickersymbol):
    return jsonify(calc_dividends(tickersymbol))

#get all dividends which will be received this year
@app.route("/dividends", methods=["GET"])
def getAllDivs():
    return jsonify(calc_all_dividends())

#delete a transaction from the securities account
@app.route("/delete//<int:transaction_id>", methods=["DELETE"])
def delTrans(transaction_id):
    return deleteEntry(transaction_id)

#display all transactions
@app.route("/transactions", methods=["GET"])
def getAllTransactions():
    return jsonify(transactions = securities_acc)

#save transactions to database file
@app.route("/save", methods=["GET"])
def save_transactions_to_database():
    save_db()
    return jsonify(success = True,
                   message = "Successfully saved transaction to database",
                   transactions = securities_acc)

# additional evaluation method - the graham number
@app.route("/graham/<tickersymbol>", methods=["GET"])
def graham(tickersymbol):
    fng = list(fear_and_greed.get())
    return getGrahamNumber(tickersymbol, fng[0])

#######################
@app.route("/")
def index():
    conn_db()
    return jsonify(
            success = True,
            message = "Your server is running! Welcome to the Daniel's dividend strategy API.",
            transactions = securities_acc)

@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] =  "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    response.headers['Access-Control-Allow-Methods']=  "POST, GET, PUT, DELETE, PATCH"
    return response

if __name__ == "__main__":
    app.run(debug=True, port=8888)

