import sqlite3
from requests import get
import urllib.parse as up
import pandas as pd

class Markit:
    def __init__(self):
        self.lookup_url = "http://dev.markitondemand.com/Api/v2/Lookup/json?"
        self.quote_url = "http://dev.markitondemand.com/Api/v2/Quote/json?"

    def company_search(self,string):
        '''returns a dictionary with keys as Symbol,Name,Exchange with corresponding
        values by lookup for string using Markit API, False if there is no result'''
        stock_info = get(self.lookup_url+up.urlencode({'input':string})).json()
        if len(stock_info)==0 or type(stock_info)==dict:
            return False
        else:
            return stock_info

    def get_stock_info(self,string):
        '''returns a dictionary with keys as Status,Name,Symbol,
        LastPrice,Change,ChangePercent,Timestamp,MSDate,MarketCap,Volume,
        ChangeYTD,ChangePercentYTD,High,Low,Open with corrensponding values by 
        get_quote for string using Markit API, False is there is no result'''
        stock_info = get(self.quote_url+up.urlencode({'symbol':string})).json()
        if len(stock_info) <= 1:
            return False
        else:
            return [stock_info]

db="database.db"
conn = sqlite3.connect(db)
cur = conn.cursor()

def save():
    '''returns None, commit the changes made to db'''
    global conn
    conn.commit()

def close_conn():
    '''returns None and closes the connection'''
    global conn
    conn.close()
    
def not_super(username):
    cur.execute('SELECT EXISTS(SELECT 1 FROM User WHERE username=? LIMIT 1)', (username,))
    return cur.fetchone()[0]    
    
def is_super(username):
    cur.execute('SELECT EXISTS(SELECT 1 FROM Super_user WHERE username=? LIMIT 1)', (username,))
    return cur.fetchone()[0]
    
def check_username(username):
    '''returns True if username is in (any of User and Super_user) TABLE and False otherwise'''
    return not_super(username) or is_super(username)

def add_user(username,password,money,is_super):
    '''returns None, INSERTS username, password, and money(optional) INTO the corresponding TABLE (determined is_super)'''
    cur.execute('INSERT INTO '+is_super*"Super_user"+abs(is_super-1)*"User"+\
                ' VALUES("'+username+'","'+password+'",'+str(money)+');')
    save()
    
def check_user(username,password):
    '''returns (True,True) if username and password matches with the username and password in Super_user TABLE or
    (True,False) if username and password matches with the username and password in User TABLE and (False) otherwise'''
    username_password = dict(cur.execute("SELECT username,password from Super_user;").fetchall())
    for username_,password_ in username_password.items():
        if username==username_ and password==password_:
            return (True,True)
    username_password = dict(cur.execute("SELECT username,password from User;").fetchall())
    for username_,password_ in username_password.items():
        if username==username_ and password==password_:
            return (True,False)
    return tuple([False])

def user_money(username,is_super):
    cur.execute('SELECT "money" FROM '+abs(is_super-1)*'User'+is_super*'Super_user'+' WHERE username = "'+username+'";')
    return cur.fetchone()[0]

def user_total_value(username,is_super):
    cur.execute('SELECT symbol, quantity FROM Stock WHERE username="'+username+'";')
    symbol_quantity = dict(cur.fetchall())
    cur.execute('SELECT symbol, last_buy_price FROM Stock_price')
    symbol_price = dict(cur.fetchall())
    stock_worth = 0
    for i in symbol_quantity.keys():
        stock_worth += symbol_price[i] * symbol_quantity[i]
    money = user_money(username,is_super)
    return [stock_worth+money,stock_worth,money]

def user_stock_list(username):
    cur.execute('SELECT symbol, quantity FROM Stock WHERE username="'+str(username)+'";')
    symbol_quantity = dict(cur.fetchall())
    symbol = list(symbol_quantity.keys())
    quantity = list(symbol_quantity.values())
    cur.execute('SELECT symbol, last_buy_price FROM Stock_price')
    symbol_price = dict(cur.fetchall())
    price = list(map(lambda asymbol: symbol_price[asymbol], symbol))
    worth = list(map(lambda i: quantity[i] * price[i], range(len(quantity))))
    return [symbol,quantity,price,worth]

def leaderboard(top_what = 10):
    cur.execute('SELECT username FROM User;')
    usernames = list(cur.fetchall())
    cur.execute('SELECT username FROM Super_user;')
    usernames.extend(list(cur.fetchall()))
    data = {}
    for i in range(len(usernames)):
        username = usernames[i][0]
        data[i] = [username] + user_total_value(username,is_super(username))
    columns = ["Username","Total Worth","Stock Worth","Money"]
    df = pd.DataFrame.from_dict(data, orient='index', columns=columns)
    df = df.sort_values(by=["Total Worth","Stock Worth"], ascending=False).head(top_what)
    return df.values.tolist(),columns

def buy_stock(username,is_super,stock_symbol,stock_price,qty):
    money = user_money(username,is_super)
    if money < stock_price * qty:
        return False
    cur.execute('UPDATE '+abs(is_super-1)*'User'+is_super*'Super_user'+' SET "money" = '+str(money - (stock_price * qty))+' WHERE "username" = "'+username+'";')
    cur.execute('UPDATE Stock SET quantity = quantity + '+str(qty)+' WHERE username = "'+username+'" AND symbol = "'+stock_symbol+'";')
    save()
    cur.execute('INSERT INTO Stock (username, symbol, quantity) SELECT "'+username+'", "'+stock_symbol+'", '+str(qty)+' WHERE (Select Changes() = 0);')
    cur.execute('UPDATE Stock_price SET last_buy_price = '+str(stock_price)+' WHERE symbol = "'+stock_symbol+'";')
    save()
    cur.execute('INSERT INTO Stock_price (symbol, last_buy_price) SELECT "'+stock_symbol+'", '+str(stock_price)+' WHERE (Select Changes() = 0);')
    save()
    return True

def get_user_stock(username,stock_symbol):
    cur.execute('SELECT quantity FROM Stock WHERE username = "'+username+'" AND symbol = "'+stock_symbol+'";')
    try:
        return cur.fetchone()[0]
    except:
        return False
    
def sell_stock(username,is_super,stock_symbol,stock_price,qty):
    if get_user_stock(username,stock_symbol) < qty:
        return False
    money = user_money(username,is_super)
    cur.execute('UPDATE '+abs(is_super-1)*'User'+is_super*'Super_user'+' SET "money" = '+str(money + (stock_price * qty))+' WHERE "username" = "'+username+'";')
    cur.execute('UPDATE Stock SET quantity = quantity - '+str(qty)+' WHERE username = "'+username+'" AND symbol = "'+stock_symbol+'";')
    save()
    cur.execute('DELETE FROM Stock WHERE quantity = 0;')
    cur.execute('UPDATE Stock_price SET last_buy_price = '+str(stock_price)+' WHERE symbol = "'+stock_symbol+'";')
    save()
    return True