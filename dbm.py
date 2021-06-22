from data import *
from os import path
import sqlite3

def conn_db():
    global conn
    global cursorObj
    # check if database already exists
    if path.isfile('./transactions.db'):
        conn = sqlite3.connect('transactions.db', check_same_thread=False)  # permit different threads
        cursorObj = conn.cursor()
        # get all rows (transaction) and add them to the securities_acc dictionary
        cursorObj.execute('SELECT * FROM transactions')
        dat = cursorObj.fetchall()
        for trans in dat:
            securities_acc[int(trans[0])] = {"stock": trans[1], "date": trans[2], "price": float(trans[3]),
                                             "number_of_shares": float(trans[4]), "dividend per share": float(trans[5])}
    else:  # if database does not exist, create one
        conn = sqlite3.connect('transactions.db', check_same_thread=False)  # permit different threads
        cursorObj = conn.cursor()
        # create the table transactions, id is text as uuid4() returns too long integer for sqlite3
        cursorObj.execute("""CREATE TABLE transactions(id text PRIMARY KEY,
        name text,
        date text,
        price real,
        number_of_shares real,
        dividend_per_share real)""")
        for t in securities_acc:  # t is transaction id
            trans = securities_acc[t]  # access transaction knowing its key
            params = (str(t), trans["stock"], trans["date"], trans["price"], trans["number_of_shares"],
                      trans["dividend per share"])
            cursorObj.execute("INSERT INTO transactions VALUES (?, ?, ?, ?, ?, ?)", params)  # insert to the table
        conn.commit()


def save_db():
    # connection is still open
    for t in securities_acc:
        try:  # add only new transactions to the database
            trans = securities_acc[t]
            params = (str(t), trans["stock"], trans["date"], trans["price"], trans["number_of_shares"],
                      trans["dividend per share"])
            cursorObj.execute("INSERT INTO transactions VALUES (?, ?, ?, ?, ?, ?)", params)
            print("Transaction successfully saved to database")
        except:
            print("Transaction already in record")
    conn.commit()
    # after saving changes close the connection
    conn.close()


def deleteEntry(transaction_id):
    # delete from transactions records and also from the database table
    if transaction_id in securities_acc:
        del securities_acc[transaction_id]
    else:
        return f"No transaction with id {transaction_id}."
    try:
        cursorObj.execute("DELETE FROM transactions WHERE id = ?", (str(transaction_id),))
    except:
        return "Deleted from temporary storage, but no open data base found."
    return securities_acc

# def conn_db():
#     global conn
#     global cursorObj
#     # check if database already exists
#     if path.isfile('./watchlist.db'):
#         conn = sqlite3.connect('watchlist.db', check_same_thread=False)  # permit different threads
#         cursorObj = conn.cursor()
#         # get all rows (stocks) and add them to the stocks list
#         cursorObj.execute('SELECT * FROM stocks')
#         dat = cursorObj.fetchall()
#         watchlist = []
#         for stock in dat:
#             watchlist.append(stock)
#         conn.commit()
#     else:  # if database does not exist, create one
#         conn = sqlite3.connect('watchlist.db', check_same_thread=False)  # permit different threads
#         cursorObj = conn.cursor()
#         # create the table watchlist
#         cursorObj.execute("""CREATE TABLE watchlist(
#         name text,
#         ticker text,
#         ISIN text PRIMARY KEY,
#         dividend_yield real,
#         branch text,
#         country text,
#         frequency real,
#         signal text,
#         current_dividend real,
#         previous_dividend real,
#         dividend_growth real,
#         five_year_average_growth real,
#         five_year_dividend_growths real)""")
#         conn.commit()
#     conn.close()
#
# def save_db(watchlist):
#     conn = sqlite3.connect('watchlist.db', check_same_thread=False)  # permit different threads
#     cursorObj = conn.cursor()
#     for stock in watchlist:
#         try:  # add only new transactions to the database
#             params = (stock.name, stock.ticker, stock.ISIN, stock.divyield,
#                       stock.branch, stock.country, stock.frequency, stock.signal, stock.currentDiv, stock.lastDiv,
#                       stock.divGrowth, stock.five_year_avg_growth, stock.growths, stock.continuity)
#             cursorObj.execute("INSERT INTO watchlist VALUES (?, ?, ?, ?, ?, ?)", params)
#             print("Transaction successfully saved to database")
#         except:
#             print("Transaction already in record")
#     conn.commit()
#     # after saving changes close the connection
#     conn.close()