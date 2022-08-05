import discord
import helper
import economey_cmd as ec
import fishing_cmd as fish
import random

TOKEN = ""


# Initilize Discord Client
client = discord.Client()

@client.event 
async def on_ready():
    print("I AM CONNECTED TO DISCORD")


# On message
@client.event
async def on_message(message):

    # if the author is the client then ignore
    if message.author == client.user:
        return


    # If the message is a command
    if message.content[0] == "!":

        # ADD COMMANDS
        elif message.content[1:len("e") + 1] == "e":

            message.content = message.content[len("e") + 2:]
            message.content = message.content.split(" ")

            if message.content[0] == "start":
                await ec.start_cmd(message)

            elif message.content[0] == "balance":
                await ec.balance_cmd(message)

            elif message.content[0] == "pay":
                await ec.pay_cmd(message)

            elif message.content[0] == "spin":
                await ec.spin_cmd(message)

            elif message.content[0] == "shop":
                await ec.shop_cmd(message)
            
            elif message.content[0] == "buy":
                await ec.buy_cmd(message)
                
            elif message.content[0] == "flexall":
                await ec.flexall_cmd(message)
            
            elif message.content[0] == "flex":
                await ec.flex_cmd(message)
            
            elif message.content[0] == "stock":
                await ec.stock_cmd(message)
            
            elif message.content[0] == "cf":
                wallets = helper.read_file(["wallets", "wallets"])
                if wallets[message.author.name]["balance"] >= round(float(message.content[1]), 2):
                    coin_flip = random.randint(0, 1)
                    if coin_flip == 0:
                        wallets[message.author.name]["balance"] -= round(float(message.content[1]), 2)
                        await message.channel.send(":x: You Lost " + str(round(float(message.content[1]), 2)) + " Points! :x:")
                    else:
                        wallets[message.author.name]["balance"] += round(float(message.content[1]), 2)
                        await message.channel.send(":white_check_mark: You Won " + str(round(float(message.content[1]), 2)) + " Points! :white_check_mark:")
                    helper.write_file(["wallets", "wallets"], wallets)
                else:
                    await message.channel.send("You dont have that much money!")
            
            elif message.content[0] == "fish":
                await fish.fishing_cmd(message)
    
    
    else:
        await message.channel.send("commands must start with !e"




client.run(TOKEN)
