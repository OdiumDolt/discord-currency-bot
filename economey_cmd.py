from traceback import print_tb
import helper
import time
import random
import discord
async def start_cmd(message):   
    wallets = helper.read_file(["wallets", "wallets"])
    wallets[message.author.name] = {
        "balance":0,
        "stocks":{},
        "flex_items":{},
        "wheel_spin_timer":round(time.time()),
        "fishing":{
        "current_fish":{}, 
        "cool_down":0
        }

    }
    helper.write_file(["wallets", "wallets"], wallets)
    await message.channel.send("Wallet has been created!")
    
async def balance_cmd(message):
    # Balance Command
    wallets = helper.read_file(["wallets", "wallets"])
    try:
        balance = wallets[message.author.name]["balance"]
    except KeyError:
        await message.channel.send("Please initialize your wallet with !e start")

    if balance < 1000:
        await message.channel.send("You currently have " + str(balance) + """ points.
get your money up""")
    elif balance > 1000 and balance < 10000:
        await message.channel.send("You currently have " + str(balance) + " points")
    else:
        await message.channel.send("You currently have " + str(balance) + """ points.
You breaded up g.""")
            
async def pay_cmd(message):
    # Pay Command
    try:
        wallets = helper.read_file(["wallets", "wallets"])
        recipent = wallets[message.content[1]]
    except KeyError:
        await message.channel.send("That person doesnt exist")
        return 0
        
    if message.content[2] == "flex":
        try:
            item = wallets[message.author.name]["flex_items"][message.content[3]]
            if item["quantity"] > 0:
                item["quantity"] -= 1
                if item["quantity"] == 0:
                    del wallets[message.author.name]["flex_items"][message.content[3]]

                try:
                    recipent["flex_items"][message.content[3]]["quantity"] += 1
                except KeyError:
                    wallets[message.content[1]]["flex_items"][message.content[3]] = item
                    wallets[message.content[1]]["flex_items"][message.content[3]]["quantity"] = 1

                helper.write_file(["wallets", "wallets"], wallets)
                await message.channel.send("Payment Completed!")
        except KeyError:
            await message.channel.send("You dont own that flex item :gorilla:")

        
    elif round(float(message.content[2]), 2) > 0:
        message.content[2] = round(float(message.content[2]), 2)
        if wallets[message.author.name]["balance"] >= round(message.content[2], 2):
            wallets[message.author.name]["balance"] -= round(message.content[2], 2)
            wallets[message.content[1]]["balance"] += round(message.content[2], 2)
            helper.write_file(["wallets", "wallets"], wallets)
            await message.channel.send("Payment Completed!")
        else:
            await message.channel.send("I'm sorry, You dont seem to have enough for that payment")
            await message.channel.send("Maybe you should get more bread, you poor broke boy. Make your money work for you.")
    else:
        await message.channel.send("I dont understand that!")

async def spin_cmd(message):
    # Spin Command
    wallets = helper.read_file(["wallets", "wallets"])
    if wallets[message.author.name]["wheel_spin_timer"] + 3600 <= time.time():
        is_one = random.randint(0, 100)
        await message.channel.send("Spinning...")
        time.sleep(1)
        if is_one == 1:
            winnings = 1
            await message.channel.send("Congratulations, you gained " + str(winnings) + " points!")
            time.sleep(2)
            await message.channel.send("""Bruh wtf. Your actually dog water. How the fuck do you roll a one. There's literally a 5% chance of that happening. Lame ass bitch.""")
        else:
            winnings = random.randint(20, 100)
            await message.channel.send("Congratulations, you gained " + str(winnings) + " points!")
        wallets = helper.read_file(["wallets", "wallets"])
        wallets[message.author.name]["balance"] += winnings
        wallets[message.author.name]["wheel_spin_timer"] = time.time()
        helper.write_file(["wallets", "wallets"], wallets)
    else:
        await message.channel.send("You need to wait " + str(round((3600 - (time.time() - wallets[message.author.name]["wheel_spin_timer"]))/60, 2)) + " minutes")
            
async def shop_cmd(message):
    flex_items = helper.read_file(["flex_items", "flex_items"])
    send_message = "The Shop:"
    for i in flex_items:
        send_message += "\n" + i + ", Cost: " + str(flex_items[i]["cost"]) + ", Quantity: " + str(flex_items[i]["quantity"]) 
    await message.channel.send(send_message)

async def buy_cmd(message):
    wallets = helper.read_file(["wallets", "wallets"])
    flex_items = helper.read_file(["flex_items", "flex_items"])
    selected_item = flex_items[message.content[1].replace(" ", "_").lower()]
    id = message.content[1].replace(" ", "_").lower()
    if wallets[message.author.name]["balance"] >= selected_item["cost"]:
        selected_item["quantity"] -= 1

        try:
            wallets[message.author.name]["flex_items"][id]["quantity"] += 1
        except KeyError:
            wallets[message.author.name]["flex_items"][id] = {
                "quantity":1,
                "name": id,
                "location": flex_items[id]["location"]
            }

        wallets[message.author.name]["balance"] -= selected_item["cost"]
        await message.channel.send("You have succesfully purchased a " + id + " token!")

        if selected_item["quantity"] == 0:
            del flex_items[id]
        helper.write_file(["flex_items", "flex_items"], flex_items)
        helper.write_file(["wallets", "wallets"], wallets)
    else:
        await message.channel.send("You dont got the bread for that")

async def flexall_cmd(message):
    flex = helper.read_file(["wallets", "wallets"])[message.author.name]
    send_message = "Your tokens:"
    for i in flex["flex_items"]:
        send_message += "\n" + i + ": " + str(flex["flex_items"][i]["quantity"])
    await message.channel.send(send_message)


async def flex_cmd(message):
    wallet = helper.read_file(["wallets", "wallets"])[message.author.name]
    try:
        item = wallet["flex_items"][message.content[1]]
        await message.channel.send(file=discord.File(item["location"]))
    except:   
        await message.channel.send("You dont own that monkey :monkey:")

async def stock_cmd(message):

    stocks, wallets = helper.update_stocks()


    if message.content[1] == "buy":
        try:
            if stocks["stocks"][message.content[2]]["price"] * int(message.content[3]) <= wallets[message.author.name]["balance"]:
                try:
                    wallets[message.author.name]["stocks"][message.content[2]]["shares"] += int(message.content[3])
                except KeyError:
                    wallets[message.author.name]["stocks"][message.content[2]] = {
                        "buying_price":stocks["stocks"][message.content[2]]["price"],
                        "shares": int(message.content[3])
                    }
                await message.channel.send("You succesfully purchased " + str(message.content[3]) + " shares of " + str(message.content[2]) + " for " + str(round(stocks["stocks"][message.content[2]]["price"] * int(message.content[3]), 2)) + " points! :dollar: :dollar:")
                wallets[message.author.name]["balance"] = round(wallets[message.author.name]["balance"] - (stocks["stocks"][message.content[2]]["price"] * int(message.content[3])), 2)
                helper.write_file(["wallets", "wallets"], wallets)
            else:
                await message.channel.send("You dont have enough money for that :see_no_evil:")
        except KeyError:    
            await message.channel.send("That stock doesent exist!")

    elif message.content[1] == "sell":
        try:
            if int(message.content[3]) <= wallets[message.author.name]["stocks"][message.content[2]]["shares"]:
                wallets[message.author.name]["balance"] += round(stocks["stocks"][message.content[2]]["price"] * int(message.content[3]), 2)
                await message.channel.send("You have sold, " + message.content[3] + " shares of " + message.content[2] + " for " + str(stocks["stocks"][message.content[2]]["price"] * int(message.content[3])))
                
                wallets[message.author.name]["stocks"][message.content[2]]["shares"] -= int(message.content[3])
                if wallets[message.author.name]["stocks"][message.content[2]]["shares"] == 0:
                    del wallets[message.author.name]["stocks"][message.content[2]]
                helper.write_file(["wallets", "wallets"], wallets)
        except KeyError:
            await message.channel.send("You dont own that stock!")
            
    
    elif message.content[1] == "price":
        send_message = "Stocks: "
        for i in stocks["stocks"]:
            send_message += "\n" + i + ", $" + str(stocks["stocks"][i]["price"])
        await message.channel.send(send_message)

    elif message.content[1] == "balance":
        send_message = "Your Stocks: "
        for i in wallets[message.author.name]["stocks"]:
            send_message += "\n" + i + ": " + str(wallets[message.author.name]["stocks"][i]["shares"]) + " shares, ROI: " + str(round((((stocks["stocks"][i]["price"] * wallets[message.author.name]["stocks"][i]["shares"])/(wallets[message.author.name]["stocks"][i]["buying_price"] * wallets[message.author.name]["stocks"][i]["shares"])) - 1) * 100, 2)) + "%"
        await message.channel.send(send_message)
