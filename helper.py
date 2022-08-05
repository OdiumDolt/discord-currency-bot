import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import matplotlib.pyplot as plt
 

# init firebase database
cred = credentials.Certificate('./currency-bot-TEST.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

from math import floor
import random
import time


# read from database
def read_file(location):
    return db.collection(location[0]).document(location[1]).get().to_dict()

# write from database
def write_file(location, data):
    db.collection(location[0]).document(location[1]).set(data)

# find the bad workds people have said
def find_words(message, words):
    bad_words = {}
    # initlize bad word counter
    # TODO init this in a faster way. Maybe once in the main file
    for i, index in enumerate(words):
        bad_words[index] = 0

    # for every catergory
    for category in words:
        # for every word in that catagory
        for word in words[category]:
            # avoid uppercase spelling
            temp_message = message.lower()
            # go through the whole message until no more words can be found
            while True:
                if temp_message.find(word.lower()) != -1:
                    bad_words[category] += 1
                    temp_message = temp_message[message.find(word.lower()) + len(word):]
                else:
                    break

    return bad_words


def update_stocks():
    stocks = read_file(["stocks", "stocks"])
    wallets = read_file(["wallets", "wallets"])
    
    # calcutalte the amount of time has passed in hours
    repeats = floor((time.time() - stocks["info"]["last_update"])/3600)
    # find the reminder amount of time
    remainder = (((time.time() - stocks["info"]["last_update"])/3600) - repeats) * 3600


    # check if the stock has been updated to avoid writing when not required
    daily_updated = False
    monthly_updated = False
    for i in range(repeats):
        for i in stocks["stocks"]:
            # calculate the stocks fluctuations
            g_or_l = random.choices(["high_gain", "low_gain", "low_loss", "high_loss"], weights=stocks["stocks"][i]["price_changes"])[0]
            change = round(random.uniform(stocks["stocks"][i]["value_change"][g_or_l][0], stocks["stocks"][i]["value_change"][g_or_l][1]), 2)
            stocks["stocks"][i]["price"] = round(change * stocks["stocks"][i]["price"], 2)

            # add the stock price to the history
            stocks["stocks"][i]["history"]["daily"].append(stocks["stocks"][i]["price"])

            # check if the stock 
            if len(stocks["stocks"][i]["history"]["daily"]) == 24:
                monthly_updated = True
                stocks["stocks"][i]["history"]["monthly"].append(stocks["stocks"][i]["history"]["daily"][-1])
                stocks["stocks"][i]["history"]["daily"] = []
                stocks["stocks"][i]["history"]["daily"] = [stocks["stocks"][i]["price"]]

        daily_updated = True
    
    if daily_updated == True:
        # set the last update to true
        stocks["info"]["last_update"] = time.time() - remainder
        
        for i in stocks["stocks"]:
            set_stock_graph(stocks, i, "daily")

        if monthly_updated == True:
            for i in stocks["stocks"]:
                set_stock_graph(stocks, i, "monthly")

        write_file(["stocks", "stocks"], stocks)

    return reset_stocks(stocks, wallets)

def reset_stocks(stocks, wallets):
    if time.time() - stocks["info"]["last_month"] > 2628333.33333:
        for i in wallets:
            for j in list(wallets[i]["stocks"]):
                wallets[i]["balance"] += round(stocks["stocks"][j]["price"] * wallets[i]["stocks"][j]["shares"])
                del wallets[i]["stocks"][j]
        

        for i in stocks["stocks"]:
            stocks["stocks"][i]["history"]["monthly"] = []
            stocks["stocks"][i]["history"]["daily"] = []

        stocks["stocks"]["BRA"]["price"] = 10
        stocks["stocks"]["RHN"]["price"] = 350
        stocks["stocks"]["EME"]["price"] = 250
        stocks["stocks"]["HUM"]["price"] = 500
        stocks["stocks"]["DANG"]["price"] = 50
        repeats = floor((time.time() - stocks["info"]["last_month"])/2628333.33333)
        remainder = (((time.time() - stocks["info"]["last_month"])/2628333.33333) - repeats) * 2628333.33333
        stocks["info"]["last_month"] = time.time() - remainder
        
        for i in stocks["stocks"]:

            set_stock_graph(stocks, i, "daily", delete_graphs="daily")
            set_stock_graph(stocks, i, "monthly", delete_graphs="monthly")

        write_file(["stocks", "stocks"], stocks)
        write_file(["wallets", "wallets"], wallets)

    return stocks, wallets

def set_stock_graph(stocks, stock, time, delete_graphs=None):
    if delete_graphs == None:
        y = stocks["stocks"][stock]["history"][time]
        x = []
        for i in range(len(y)):

            x.append(i)

        plt.figure(stock)
        plt.plot(x, y)
        plt.title(time + " prices of " + stock)
        plt.xlabel("time")
        plt.ylabel("price")
        plt.savefig("graphs/" + stock + "_" + time + ".png")
        plt.figure(stock).clf()
    elif delete_graphs == "monthly":
        x = []
        y = []
        plt.figure(stock)
        plt.title(time + " prices of " + stock)
        plt.xlabel("time")
        plt.ylabel("price")
        plt.savefig("graphs/" + stock + "_" + time + ".png")
        plt.figure(stock).clf()
    elif delete_graphs == "daily":
        x = []
        y = []
        plt.figure(stock)
        plt.title(time + " prices of " + stock)
        plt.xlabel("time")
        plt.ylabel("price")
        plt.savefig("graphs/" + stock + "_" + time + ".png")
        plt.figure(stock).clf()