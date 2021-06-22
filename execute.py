from data import *
from Stock import *
from calculations import *

### remarks ###
# missing data persistance is annoying
# the calculations take too long, especially if i need to do them every time
# needed: data persistance (safe ticker of watchlist and only load those)
# needed: an interface with buttons for every function

inp = input("Do you wish to filter your stocks list? ").lower()[0]
if inp == "y":
    watchlist = filter_Stocks(stocks)
    calculate_watchlist(watchlist)
    print([stock.serialize() for stock in watchlist])
else:
    calculate_watchlist(stocks)
    print([stock.serialize() for stock in stocks])

fng = list(fear_and_greed.get())
print(fng)
print(stocks.serialize() for stock in watchlist if stock.signal == "buy")


