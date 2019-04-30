import discord
import json
import random
import os
from markov_update import createMarkovJSONUser

client = discord.Client()

# getMarkovJSONDict
# Attempts to get a JSON dictionary for the specified user, getting the channel from the message sent. If it cannot find one, it will then call createMarkovJSONUser to create one - then use that.

def getMarkovJSONDict(message, user):
    jsonFileName = str(user.id) + "-" + str(message.guild.id) + "-" + str(message.channel.id) + ".json"
    if os.path.isfile(jsonFileName):
        next
    else:
        createMarkovJSONUser(message, user)
    with open(jsonFileName) as jsonFile:
        jsonDict = json.load(jsonFile)
        return jsonDict
    
# makeMarkovChain
# Uses the specified dictionary to create a Markov chain - with the operands given. If no operands are given: Chooses a first word from the "<start>" list (It will automatically end if it chooses an "<end>" list, Length would be a random number between 3 and 14

def createMarkovChain(markovDict, startingString, chainLength):
    markovChain = []

    if chainLength == 0:
        chainLength = random.randint(3,16)
    if startingString == "":
        startingString = "<start>"
    else:
        if startingString not in markovDict["<items>"]:
            startingString = "<start>"
        else:
            markovChain.append(startingString)

    newWord = random.choice(markovDict["<items>"][startingString])
    while len(markovChain) < chainLength and newWord != "<end>":
        markovChain.append(newWord)
        newWord = random.choice(markovDict["<items>"][newWord])
    
    returnChain = " ".join(markovChain)

    return(returnChain)