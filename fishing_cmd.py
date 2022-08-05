import re
import time
import helper
import random

async def fishing_cmd(message):
    wallets = helper.read_file(["wallets", "wallets"])
    
    # IF THE COMMAND IS A START
    if message.content[1] == "start": 

        try:
            if wallets[message.author.name]["fishing"]['cool_down'] + 60 <= time.time():
                # wallets[message.author.name]["fishing"]["cool_down"] = time.time()
                
                wait = random.randint(1, 3)
                wallets[message.author.name]["fishing"]["current_fish"]["catch_time"] = wait * 5 + time.time()
                water_emojis = ""
                for i in range(wait):
                    water_emojis += ":droplet:"
                await message.channel.send("You cast your line " + message.author.name + "! " + water_emojis)
                helper.write_file(["wallets", "wallets"], wallets)
            else:
                await message.channel.send("You must wait " + str(time.time()) + " to fish! :tropical_fish:")
        except KeyError:
            await message.channel.send("Please start your wallet before you fish :shark:")

    # IF THE COMMAND IS A CATCH
    elif message.content[1] == "catch": 
        TIMING = 1
        # check if the timing of the catch is within the timing window
        if wallets[message.author.name]["fishing"]['current_fish']["catch_time"] + TIMING >= time.time() and wallets[message.author.name]["fishing"]['current_fish']["catch_time"] - TIMING <= time.time():
            
            # 
            reward = random.randint(1, 1000)
            if reward <= 5:
                fishing_items = helper.read_file(["flex_items", "fishing_items"])
                options = ["angeo_pause", "eme_baby", "eme_cbum", "hummus_ass", "hummus_valentine", "jo_happy", "rohn_upset"]
                item = random.choices(options, weights=[8, 30, 10, 2, 20, 15, 15])[0]
                try:
                    wallets[message.author.name]["flex_items"][item]["quantity"] += 1
                except KeyError:
                    wallets[message.author.name]["flex_items"][item] = {
                        "location":fishing_items[item]["location"],
                        "quantity":1,
                        "name":item
                    }
                await message.channel.send("Lucky! You fished up a Flex Item! You recieved 1 " + item + "! :frame_photo:")
                helper.write_file(["wallets", "wallets"], wallets)
            elif reward > 6 and reward < 55:
                await message.channel.send("You pulled up a boot... :hiking_boot:")
            else:
                money = round(random.uniform(1, 0.1), 2)
                wallets[message.author.name]["balance"] += round(money, 2)
                await message.channel.send("You found a fish! :fishing_pole_and_fish: You sold it for $" + str(money) + " :dollar:")
                helper.write_file(["wallets", "wallets"], wallets)
        
        
        elif wallets[message.author.name]["fishing"]['current_fish']["catch_time"] + 1 < time.time():
            await message.channel.send("You reeled in too slow, calm down silly. :snail:")
        elif wallets[message.author.name]["fishing"]['current_fish']["catch_time"] - 1 > time.time():
            await message.channel.send("You reeled in too fast, slow the fuck down. :man_in_motorized_wheelchair:")
        else:
            await message.channel.send("You were to slow! :shrimp:")
