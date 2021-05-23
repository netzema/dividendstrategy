from dbm import *
from random import choice
import os

# here we will test the dbm.py code by implementing the same code stepwise with a temporary database file test.db

def test_conn_db():
    securities_acc = {}
    # start first connection, create file
    conn = sqlite3.connect('test.db', check_same_thread=False)  # permit different threads
    cursorObj = conn.cursor()
    # create the table transactions, id is text as uuid4() returns too long integer for sqlite3
    cursorObj.execute("""CREATE TABLE transactions(id text PRIMARY KEY,
            name text,
            date text,
            price real,
            number_of_shares real,
            dividend_per_share real)""")
    # write to the file!
    params = (str(155613548235), "TestStock", "2020-05-23", 45.45, 10, 0.59)
    cursorObj.execute("INSERT INTO transactions VALUES (?, ?, ?, ?, ?, ?)", params)  # insert to the table
    conn.commit()
    conn.close()
    # after finishing, check if the file was created
    assert path.isfile('./test.db')

    # connect to the file again
    conn = sqlite3.connect('test.db', check_same_thread=False)  # permit different threads
    cursorObj = conn.cursor()
    # get all rows of file - must be one, as we inserted one before
    cursorObj.execute('SELECT * FROM transactions')
    dat = cursorObj.fetchall()
    for trans in dat:
        securities_acc[int(trans[0])] = {"stock": trans[1], "date": trans[2], "price": float(trans[3]),
                                         "number_of_shares": float(trans[4]), "dividend per share": float(trans[5])}
    # check if the new entry is now in securities account
    assert len(securities_acc) > 0
    conn.commit()
    conn.close()
    # delete file again
    os.remove("test.db")

def test_save_db():
    # start with an entry in securites account and create database file
    securities_acc = {478903479358734: {"stock": "TestStock", "date": "2020-05-23", "price": 45.45,
                                        "number_of_shares": 10, "dividend per share": 0.59}}
    conn = sqlite3.connect('test.db', check_same_thread=False)  # permit different threads
    cursorObj = conn.cursor()
    cursorObj.execute("""CREATE TABLE transactions(id text PRIMARY KEY,
                name text,
                date text,
                price real,
                number_of_shares real,
                dividend_per_share real)""")
    # add transactions from securities account to newly created database file
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
    # reset securities account variable and connect again to the file
    securities_acc = {}
    conn = sqlite3.connect('test.db', check_same_thread=False)  # permit different threads
    cursorObj = conn.cursor()
    # get all rows (transaction) and add them to the securities_acc dictionary
    # write from previously saved database file to securities account again
    cursorObj.execute('SELECT * FROM transactions')
    dat = cursorObj.fetchall()
    for trans in dat:
        securities_acc[int(trans[0])] = {"stock": trans[1], "date": trans[2], "price": float(trans[3]),
                                         "number_of_shares": float(trans[4]), "dividend per share": float(trans[5])}
    # securities account must have an entry now
    assert len(securities_acc) > 0
    conn.commit()
    conn.close()
    # remove test database
    os.remove("test.db")

def test_deleteEntry():
    # start with an entry in securities account and create test database file
    securities_acc = {478903479358734: {"stock": "TestStock", "date": "2020-05-23", "price": 45.45,
                                        "number_of_shares": 10, "dividend per share": 0.59}}
    conn = sqlite3.connect('test.db', check_same_thread=False)  # permit different threads
    cursorObj = conn.cursor()
    # create the table transactions, id is text as uuid4() returns too long integer for sqlite3
    cursorObj.execute("""CREATE TABLE transactions(id text PRIMARY KEY,
                name text,
                date text,
                price real,
                number_of_shares real,
                dividend_per_share real)""")
    params = (str(478903479358734), "TestStock", "2020-05-23", 45.45, 10, 0.59)
    transaction_id = 478903479358734
    # write entry to database file
    cursorObj.execute("INSERT INTO transactions VALUES (?, ?, ?, ?, ?, ?)", params)  # insert to the table
    conn.commit()
    conn.close()
    # connect to file again and delete the entry again
    conn = sqlite3.connect('test.db', check_same_thread=False)  # permit different threads
    cursorObj = conn.cursor()
    del securities_acc[transaction_id]
    cursorObj.execute("DELETE FROM transactions WHERE id = ?", (str(transaction_id),))
    conn.commit()
    conn.close()
    # check if securities account is empty again
    assert len(securities_acc) == 0
    # connect again to database file and write to securities account again
    conn = sqlite3.connect('test.db', check_same_thread=False)  # permit different threads
    cursorObj = conn.cursor()
    # get all rows (transaction) and add them to the securities_acc dictionary
    cursorObj.execute('SELECT * FROM transactions')
    dat = cursorObj.fetchall()
    for trans in dat:
        securities_acc[int(trans[0])] = {"stock": trans[1], "date": trans[2], "price": float(trans[3]),
                                         "number_of_shares": float(trans[4]), "dividend per share": float(trans[5])}
    # due to previous deletion of the entry, the securities account must still be empty
    assert len(securities_acc) == 0
    conn.commit()
    conn.close()
    # remove file again
    os.remove("test.db")
