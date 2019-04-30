import discord
import json
import datetime
import os

client = discord.client
dir_path = os.path.dirname(os.path.realpath(__file__)) + "\\jsons\\"

# createMarkovJSONFull
# Grabs the specified number of messages (0 = all) from the specified message's channel. It creates a seperate Markov Dictionary JSON file for each user. Should overwrite existing files completely. With larger servers that have large message counts, this often takes a long time


async def createMarkovJSONFull(message, messageCount):
    userMessageList = {}
    messageCount = 1000000
    currDateTime = datetime.datetime.now().isoformat()

    print("$:Beginning channel history processing")

    async for item in message.channel.history(limit=messageCount):
        if "!markov" in str(item.content) or "!mk" in str(item.content):
            next
        elif str(item.author.id) in userMessageList:
            userMessageList[str(item.author.id)] += (
                " <start> " + str(item.content) + " <end> ")
        else:
            userMessageList[str(item.author.id)] = (
                " <start> " + str(item.content) + " <end> ")
    
    print("$:Channel history processing complete")

    for key in userMessageList:
        markovDict = {'<historyDateTime>': currDateTime, '<items>': {}}
        markovIterable = userMessageList[key].split()
        for i in range(len(markovIterable) - 1):
            line1 = markovIterable[i]
            line2 = markovIterable[i + 1]
            if markovIterable[i] in markovDict["<items>"]:
                markovDict["<items>"][line1].append(line2)
            else:
                markovDict["<items>"][line1] = [line2]
        jsonFileName = dir_path + str(key) + "-" + str(message.guild.id) + "-" + str(message.channel.id) + ".json"
        with open(jsonFileName, "w") as jsonFile:
            jsonFile.truncate(0)
            json.dump(markovDict, jsonFile)
            print("$:'" + jsonFileName + "' exported as '" + currDateTime + "'")
            print("")

    print("$:Channel dictionary creation complete")
    print("")
    return

# updateMarkovJSONFull
# Grabs each user from a channel, checks if their JSON file exists, then pulls dictionary data from it. Gets a list of messages and compares message dates for accounts to pulled dictionary data - updating the pulled dictionary with that data. Writes new dictionary to existing JSON files.

async def updateMarkovJSONFull(message, messageCount):
    userMessageList = {}
    currDateTime = datetime.datetime.now().isoformat()
    jsonList = {}

    for mkUser in message.guild.members:
        jsonFileName = dir_path + str(mkUser.id) + "-" + str(message.guild.id) + "-" + str(message.channel.id) + ".json"
        if os.path.isfile(jsonFileName):
            with open(jsonFileName) as jsonFile:
                i = json.load(jsonFile)
                jsonList[mkUser.id] = i   

    print("$:Beginning channel history processing")

    async for item in message.channel.history(limit=10000):
        if "!markov" not in str(item.content) and "!mk" not in str(item.content):
            exists = bool
            try:
                if jsonList[item.author.id] != "":
                    exists = True
                    print (jsonList[str(item.author.id)])
                    print (jsonList[str(item.author.id)]["<historyDateTime>"])
                    print (jsonList[str(item.author.id)]["<historyDateTime>"][0])
            except:
                exists = False
            if exists:
                if item.created_at.isoformat() > jsonList[str(item.author.id)]["<historyDateTime>"][0]:
                    next
                elif str(item.author.id) in userMessageList:
                    userMessageList[str(item.author.id)] += (" <start> " + str(item.content) + " <end>")
                else:
                    userMessageList[str(item.author.id)] = (" <start> " + str(item.content) + " <end>")

    print("$:Channel history processing complete")

    for key in userMessageList:
        print(key)
        markovIterable = userMessageList[key].split()
        jsonList[key]["<historyDateTime>"] = currDateTime
        jsonFileName = dir_path + str(key) + "-" + str(message.guild.id) + "-" + str(message.channel.id) + ".json"
        for i in range(len(markovIterable) - 1):
            line1 = markovIterable[i]
            line2 = markovIterable[i + 1]
            if line1 in jsonList[key]["<items>"]:
                jsonList[key]["<items>"][line1].append(line2)
            else:
                jsonList[key]["<items>"][line1] = [line2]
        with open(jsonFileName, "w") as jsonFile:
            jsonFile.truncate(0)
            json.dump(jsonList, jsonFile)
            print("$:'" + jsonFileName + "' updated to '" + currDateTime + "'")
            print("")

    print("$:Channel dictionary update complete")
    print("")
    return

# createMarkovJSONUser
# Same as the create full, except only for a user. messageCount for this is automatically set to pull all messages and cannot be adjusted

async def createMarkovJSONUser(message, user):
    userMessageList = ""
    currDateTime = datetime.datetime.now().isoformat()
    jsonFileName = dir_path + str(user.id) + "-" + str(message.guild.id) + "-" + str(message.channel.id) + ".json"
    if user == "":
        user = message.author

    print("$:Beginning channel history processing")

    async for item in message.channel.history(limit=100000):
        if item.author.id == user.id:
            if "!markov" in str(item.content) or "!mk" in str(item.content):
                next
            else:
                userMessageList += (" <start> " + str(item.content) + " <end> ")

    print("$:Channel history processing complete")

    markovDict = {'<historyDateTime>': currDateTime, '<items>': {}}
    markovIterable = userMessageList.split()
    for i in range(len(markovIterable) - 1):
        line1 = markovIterable[i]
        line2 = markovIterable[i + 1]
        if markovIterable[i] in markovDict["<items>"]:
            markovDict["<items>"][line1].append(line2)
        else:
            markovDict["<items>"][line1] = [line2]

    with open(jsonFileName, "w") as jsonFile:
        jsonFile.truncate(0)
        json.dump(markovDict, jsonFile)
        print("$:'" + jsonFileName + "' exported as '" + currDateTime + "'")
        print("")
    return

# updateMarkovJSONUser
#  Same as the update full, except only for a user. messageCount for this is automatically set to 6000 and cannot be adjusted

async def updateMarkovJSONUser(message, user):
    userMessageList = ""
    currDateTime = datetime.datetime.now().isoformat()
    jsonFileName = dir_path + str(message.author.id) + "-" + str(message.guild.id) + "-" + str(message.channel.id) + ".json"

    with open(jsonFileName) as jsonFile:
        i = json.load(jsonFile)
        jsonList = i

    async for item in message.channel.history(limit=6000):
        if "!markov" not in str(item.content) and "!mk" not in str(item.content):
                if item.created_at.isoformat() > jsonList["<historyDateTime>"][0]:
                    next
                else:
                    userMessageList += (" <start> " + str(item.content) + " <end>")

    markovIterable = userMessageList.split()
    jsonList["<historyDateTime>"] = currDateTime
    jsonFileName = dir_path + str(user.id) + "-" + str(message.guild.id) + "-" + str(message.channel.id) + ".json"
    for i in range(len(markovIterable) - 1):
        line1 = markovIterable[i]
        line2 = markovIterable[i + 1]
        if line1 in jsonList["<items>"]:
            jsonList["<items>"][line1].append(line2)
        else:
            jsonList["<items>"][line1] = [line2]
    with open(jsonFileName, "w") as jsonFile:
        jsonFile.truncate(0)
        json.dump(jsonList, jsonFile)
        print("$:'" + jsonFileName + "' updated to '" + currDateTime + "'")
        print("")
    return