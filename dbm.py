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
    global conn
    global cursorObj
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
    del securities_acc[transaction_id]
    cursorObj.execute("DELETE FROM transactions WHERE id = ?", (str(transaction_id),))
    return securities_acc
