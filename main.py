import discord
import helper
import economey_cmd as ec
import fishing_cmd as fish
import random

# A list of bad words that people should not say.
bad_words = {
    "n word":["nigga", "nigger"],
    "gay things":["faggot", "im gay", "i like dick", "i like men", "i suck dick", 
    "i want 10 big black men to ejaculate on my spine", "cum is tasty", "nut in my mouth",
    "i play chamber", "cum"],
    "cringe":["pog", "fortnite", "why am i the designated bully person", "rgx", "i deserve gold",
    "nle chopper", "rocket league", "among us", "i never bought a op", "saxophone instrumental", 
    "billie eilish by armani white", "uwu", "old town road", "genshin"]
}

TOKEN = "MTAwNDg1ODY0MzUzNzE5OTE3Ng.G83AV7.HR0lZq9ZH5kWHIGugwSr5Xb2As4TPMin4L-BFw"


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

        # Send a formated list of a persons bad words
        if message.content[1:len("badwords") + 1] == "badwords":
            try:
                message.content = message.content[len("badwords") + 2:]
                user = helper.read_file(["user_data", "user_data"])[message.content.lower()]
                send_data = message.content + " has said:"
                for i in user:
                    send_data += "\n" + i + ": " + str(user[i])
                await message.channel.send(send_data)
            except KeyError:
                await message.channel.send("That person hasn't said anything yet")

        # THE ECO COMMANDS
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
                    await message.channel.send("You dont have that much you monkey :monkey:")
            
            elif message.content[0] == "fish":
                await fish.fishing_cmd(message)
    
    
    else:

        have_said = helper.find_words(message.content, bad_words)

        try:
            user_data = helper.read_file(["user_data", "user_data"])
            user_data[message.author.name.lower()]
        except KeyError:
            user_data[message.author.name.lower()] = {}
            for i in bad_words:
                user_data[message.author.name.lower()][i] = 0
        
        for i in have_said:
            user_data[message.author.name.lower()][i] += have_said[i]

        if len(have_said) != 0:
            helper.write_file(["user_data", "user_data"], user_data)




client.run(TOKEN)
