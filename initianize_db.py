import sqlite3
import pandas as pd

initial_money = 100000
conn=sqlite3.connect("database.db")
cur=conn.cursor()

cur.execute("DROP TABLE IF EXISTS User;")
cur.execute("DROP TABLE IF EXISTS Super_user;")
cur.execute("DROP TABLE IF EXISTS Stock;")
cur.execute("DROP TABLE IF EXISTS Stock_price;")
conn.commit()

cur.execute("CREATE TABLE User(username TEXT PRIMARY KEY, password TEXT, money REAL);")
cur.execute("CREATE TABLE Super_user(username TEXT PRIMARY KEY, password TEXT, money REAL);")
cur.execute("CREATE TABLE Stock(username TEXT, symbol TEXT, quantity INTEGER)")
cur.execute("CREATE TABLE Stock_price(symbol TEXT, last_buy_price REAL);")
conn.commit()

cur.execute("INSERT INTO User VALUES('ujwal','p12345',"+str(initial_money)+");")
cur.execute("INSERT INTO Super_user VALUES('uji','p12345',"+str(initial_money)+");")
conn.commit()

conn.close()