import lame_menu as menu
import pandas as pd

yes = ("y","yes","ok","k","yeah","yah","sure","why not","of course")
no = ("n","no")

# Show functions
def show_welcome():
    return print("Welcome to Stock Terminal Application!\n")

def show_login():
    return print("Let's login!")

def show_exit():
    return print("Thank u for using this Stock Terminal Application, see u soon :)")

def show_money(money):
    return print("The amount of money u have in ur account is $"+str(money))

def show_total_value(stock_worth,money,total_worth):
    return print("Ur account total woth is $"+str(total_worth)+", with stock worth of $"+str(stock_worth)+" and the amount of money in ur account is $"+str(money)+".")

def show_price_qty(stock_name,price,*qty):
    extra = ""
    if len(qty) > 0:
        extra = " (U own "+str(qty[0])+" shares)"
    return print("Price of "+stock_name+" stock is $"+str(price)+" each share."+extra)

def show_stock_list(symbol,quantity,price,worth):
    return print(pd.DataFrame.from_dict({"Ticker Symbol":symbol,"Quantity":quantity,"Price":price,"Worth":worth}).to_string(index = False))

def show_leaderboard(rows,columns):
    return print(pd.DataFrame(rows, columns = columns).to_string(index=False))

# Basic IO functions
def ask_input(item):
    return input("Please enter "+item+":\n")

def show_error(what_wrong):
    return print(what_wrong+", please try again.\n")

def show_done(done):
    return print("U have successfully "+done+".\n")

def show_table(json_data):
    return print(pd.DataFrame([[j for j in i.values()] for i in json_data],columns=[i for i in json_data[0].keys()]).to_string(index=False))

# Ask for input functions
def ask_company_search():
    return ask_input("a rough stock ticker symbol or a company name to search for the exact ticker symbol")
    
def ask_retrieve_market_data():
    return ask_input("an exact ticker symbol of the stock u wanna get full information")
    
def ask_continue():
    return ask_input("anything to continue")
    
def ask_register_username():
    return ask_input("a username without any spaces")

def ask_register_password():
    return ask_input("a password with at least one upper case, one lower case,"+\
                     " \none number, one of @#$, no spaces and at least 8 characters long")
def ask_login_username():
    return ask_input("your username")

def ask_login_password():
    return ask_input("your password")

def ask_back():
    if input("Would u like to go back to the menu though? (y or yes for yes and anything else for no)\n")\
       .lower() in yes:
        done_back()
        return True
    else:
        return False

def ask_stock(is_buy):
    buy_or_sell = "buy" if is_buy else "sell"
    return ask_input("the exact ticker symbol of the stock u wanna "+buy_or_sell)

def ask_qty(is_buy):
    buy_or_sell = "buy" if is_buy else "sell"
    while 1:
        qty = ask_input("the quantity u wanna "+buy_or_sell+" or enter n or no for no")
        if qty.lower() in no:
            qty = False
            return qty
        try:
            if int(qty) <= 0:
                error_qty_not_positive(qty)
                continue
            return int(qty)
        except:
            error_qty(qty)
            continue

# Show error fuctions
def error_no_results():
    return show_error("No results found")

def error_username_spaces():
    return show_error("The username shouldn't contain any spaces")
    
def error_username_taken():
    return show_error("This username has already been taken")

def error_password():
    show_error("This password does not meet the requirements")

def error_login():
    return show_error("Your username and password do not match")

def error_qty(qty):
    return show_error(qty + " is neither an integer nor n or no")

def error_qty_not_positive(qty):
    return show_error(qty + " is not a positive integer")

def error_no_money(own_money,spend_money):
    return show_error("U only have $"+str(own_money)+" in ur account, but u r trying to spend $"+str(round(spend_money, 2))+", u r in a shortage of $"+str(round(spend_money-own_money, 2)))

def error_not_own_stock():
    return show_error("U do not own this stock")

def error_no_quantity(own_qty,sell_qty):
    return show_error("U only own "+str(own_qty)+" shares, but u r trying to sell "+str(sell_qty))

# Show done functions
def done_register(is_super,username):
    user = "super user" if is_super else "user"    
    return show_done("registered as a "+user+" with the username of "+username)

def done_back():
    return show_done("gone back to the menu")

def done_login(is_super):
    user = "super user" if is_super else "user"
    return show_done("logged in as a "+user)

def done_stock(stock_name,stock_price,qty,is_buy):
    buy_or_sell = "bought" if is_buy else "sold"
    return show_done(buy_or_sell+" "+str(qty)+" shares of "+stock_name+" stock at $"+str(stock_price)+" each")

def done_logout():
    return show_done("logged out from ur account")

# Menus
def returns(option):
    '''returns option'''
    return option

def register_menu():
    '''returns "ru" if Register as a user is selected, 
    "rsu" if Register as a super user is selected'''
    rm=menu.Menu(options=[("Register as a user",returns, "ru"),("Register as a super user",returns, "rsu")])
    return rm.use()
    
def portfolio_menu():
    pm=menu.Menu(options=[("View total worth of stocks plus the money in the account",returns,"vtv"),
                          ("View list of owned stocks",returns,"vls")])
    return pm.use()
    
def begin_menu():
    '''returns "sc" if "Search for a comany's exact stock ticker symbol" is selected
    "rmd" if "Retrieve market data for a stock by ticker symbol" is selected
    "ru" if Register for a new account and Register as a user is selected
    "rsu" if Register for a new account and Register as a super user is selected
    "l" if Login with an existing account is selected
    "exit" if Exit the Stock Terminal Application is selected'''
    bm=menu.Menu(options=[("Search for a comany's exact stock ticker symbol",returns,"sc"),
                          ("Retrieve market data for a stock by ticker symbol",returns,"rmd"),
                          ("Register for a new account",register_menu),
                          ("Login with an existing account (U can buy or sell stocks only after logging in)",returns,"li"),
                          ("Exit the Stock Terminal Application",returns,"exit")],
                 title="Get stock info or Register or Login or Exit")
    return bm.use()

def logged_menu(is_leaderboard):
    lm=menu.Menu(options=[("Buy a stock",returns,"bs"),("Sell a stock",returns,"ss"),
                          ("Search for a comany's exact stock ticker symbol",returns,"sc"),
                          ("Retrieve market data for a stock by ticker symbol",returns,"rmd"),
                          ("View 'portfolio'",portfolio_menu)])
    if is_leaderboard:
        lm.add_option("View the leaderboard",returns,"lb")
    lm.add_option("Logout from ur account (U have to logout first to Exit)",returns,"lo")
    return lm.use()