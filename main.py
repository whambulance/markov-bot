import discord
import os
#from keep_alive import keep_alive
from markov_update import createMarkovJSONFull
from markov_update import updateMarkovJSONFull
from markov_update import createMarkovJSONUser
from markov_update import updateMarkovJSONUser
from markov_chain import getMarkovJSONDict
from markov_chain import createMarkovChain

token = open("token.txt", "r").read()

client = discord.Client()

def getUser(message, userstring):
    user = ""
    for foruser in message.guild.members:
        if str(userstring).lower() == str(foruser).lower():
            user = foruser
    if user == "":
        for foruser in message.guild.members:
            if str(userstring).lower() in str(foruser.display_name).lower():
                user = foruser
    if user == "":
        user = message.author
    return user

def sendHelpMessage(message):
    embed=discord.Embed(title="markov-bot", url="https://github.com/whambulance/markov-bot", description="Talks based on how others type. He's like you, but better! \nType !markov to create generate a message for you \n ", color=0x4bb4f1)
    embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/7/70/AAMarkov.jpg")
    embed.add_field(name="!mv, !markov [USER]... [OPTION]...",value="Basic syntax", inline=True)
    embed.add_field(name="-s --startswith [STR]", value="Chain starting word", inline=False)
    embed.add_field(name="-l, --length [INT]", value="Chain length (def: rand 1 - 14) (max: 100)", inline=True)
    embed.add_field(name="!mkjson",value="Update your Markov JSON Dictionary", inline=True)
    return embed

@client.event
async def on_message(message):

    if message.author.bot:
        exit

    elif ("help" in str(message.content).lower() or  "aid" in str(message.content).lower() or  "hand" in str(message.content).lower() or  "assist" in str(message.content).lower()) and ("markov" in str(message.content).lower() or "mk" in str(message.content).lower()):
        embed = sendHelpMessage(message)
        await message.channel.send(embed=embed)
    elif message.content.startswith("!mk ") or message.content.startswith("!markov ") or message.content == "!mk" or message.content == "!markov":
        user = ""
        startswith = ""
        length = 0

        splitMessage = message.content.split()
        for index, i in enumerate(splitMessage):
            if i == "-s" or i == "--startswith":
                startswith = splitMessage[index+1]
            elif index == 1 and "-" not in i:
                user = i
            elif i == "-l" or i == "--length":
                length = int(splitMessage[index+1])
        
        if user != "":
            messageUser = getUser(message, user)
        else:
            messageUser = message.author
        if length > 100:
            length = 100

        print ("$:makeMarkov -u " + messageUser.display_name + " -s " + startswith + " -l " + str(length))

        userJSONDict = getMarkovJSONDict(message, messageUser)
        markovChain = createMarkovChain(userJSONDict, startswith, length)

        if markovChain != "":
            print ("Printed: " + str(markovChain))
            print ("")
            if messageUser.display_name[0].islower():
                newnick = messageUser.display_name[0:20] + " markov"
            elif messageUser.display_name.isupper():
                newnick = messageUser.display_name[0:20] + " MARKOV"
            else:
                newnick = messageUser.display_name[0:20] + " Markov"
            me = message.guild.me
            await discord.Member.edit(me, nick=newnick)
            await message.channel.send(markovChain)
            await discord.Member.edit(me, nick="")
    
    elif ("!mkjson" in str(message.content).lower()):
        splitMessage = message.content.split()
        print ("$:" + message.content[1:999] + " by " + message.author.display_name)
        for index, i in enumerate(splitMessage):
            msgCount = None
            msgUser = ""
            if str(message.author.id) == "120242398176477186":
                if i == "createchannel":
                    print("$:<admin-json-command-createchannel>")
                    msgCount = None
                    await createMarkovJSONFull(message, msgCount)
                    return
                elif i == "createuser":
                    print("$:<admin-json-command-createuser>")
                    msgUser = getUser(message, splitMessage[index+1])
                    await createMarkovJSONUser(message, msgUser)
                    return
                #elif i == "updatechannel":
                    #print("$:<admin-json-command-updatechannel>")
                    #msgCount = None
                    #await updateMarkovJSONFull(message, msgCount)
                    #return
                elif i == "updateuser":
                    print("$:<admin-json-command-updateuser>")
                    msgUser = getUser(message, splitMessage[index+1])
                    await updateMarkovJSONUser(message, msgUser)
                    return 
        await updateMarkovJSONUser(message, message.author)

    elif ("!mktest" in str(message.content).lower()):
        splitMessage = message.content.split()
        markovJSONDict =  getMarkovJSONDict(message, message.author)
        createMarkovChain(markovJSONDict, "", 0)

#keep_alive()
client.run(token)