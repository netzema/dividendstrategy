Project Description
Automation of my Dividend Strategy

I am investing in stocks for several years now. But it was only recently when I decided to completely 
change my strategy. 

Every investor loves cash flow, especially when you do not have to work for it. Passive and constant 
cash flow is what motivates me most to keep investing more and more money in the stock market. 
Thus, I decided to preferably invest into stocks which pay dividends. Dividends from international, 
well-ran companies are payments you can most of the times rely on the next couple of decades. 
This API implementation should when being called easily and quickly be able to tell the user, what 
the current market mood is, which stock prices are below their general trend and finally retrieve and 
calculate a verdict whether to buy the stock at the current time or not. 

Important disclaimer: The calculation schema for yielding a “Buy” signal is only build upon my 
personal thoughts and what I personally see as a good schema. Please do not use this 
implementation without knowing its risks. This project does NOT include any investment 
recommendations. 

The API consists of the following functionality:

- Getting the stock data:
o Get all the relevant information from a stock knowing its ticker symbol. These 
information include the name of the stock, 52-weeks-high and 52-weeks-low and 
other relevant information.
o Get the price of a stock from a certain time.
o Get the dividend paid out per share.

- Constructing a Watchlist:
o Here we store all the potential candidate stocks to eventually buy.
o The Watchlist (WL) also shows the current mood in the stock market by displaying 
data from the Fear&Greed Index.

- Calculations:
o Calculate the general trend and map it to any given period of time in the future. This 
calculation will be made up by myself. 
o The programme will calculate the stock’s price at which I would consider buying it.
o In the end, it will be able to tell my personal recommendation whether to buy the 
stock now or not, also depending on the current market mood.

- Statistics:
o Be able to set a stock to being bought, telling the system which and how many stocks
the user bought at which price.
o Calculate the dividend the user will approximately receive.
o Show the total amount of dividends the user will receive in a year.
o Store the data to a local file.
o Retrieve the previously stored data from a local file and update it.

The API is implemented in Python using Flask. 

Summary of HTTP Methods:
/wl 
GET Returns the watchlist 
including all the stocks with 
their respective data

/buy 
GET Returns all the stocks which 
emit a “Buy” signal according 
to the calculation schema

/fng 
GET Returns the current market 
mood in form of the 
Fear&Greed-Index 

/<tickersymbol> 
GET Returns all data of one 
specific stock

/buy/<tickersymbol> 
POST Mark a stock as bought. Every 
“transaction” has its unique 
ID. Parameters: price, number 
of shares

/<tickersymbol>/price 
GET Returns the current price of a 
given stock
  
/<tickersymbol>/div 
GET Get the dividend paid out per 
share of a given stock and the 
sum of the dividend the given 
company will pay the user 
this year
  
/<tickersymbol>/threshold 
GET Return the price at which a 
given stock is considered to 
buy. Note that this does not 
automatically yield a “Buy” 
signal.
  
/<tickersymbol>/recommendation 
GET Returns the recommendation 
of a given stock. 
  
/dividends 
GET Return the sum of all 
dividends approximately 
received this year.

/save 
Save bought stocks into a 
local file

/ 
Load the saved local file
about bought stocks
/delete/<transaction_id> DELETE Delete a bought stock from 
the data

All the methods will be tested using PyTest.
