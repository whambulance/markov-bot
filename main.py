import discord
import os
import random
from keep_alive import keep_alive

client = discord.Client()

def makeMarkovList(corpus):
    data = {}
    for i in range(len(corpus)-1):
        line1 = corpus[i]
        line2 = corpus[i+1]
        if line1 != "<end>" and line2 != "<end>":
            if line1 in data:
                data[line1].append(line2)
            else:
                data[line1] = [line2]
    return data	

def makeMarkovChain(markovList, startword, length):
    word = ""
    if startword == "" or startword not in markovList:
        while word[:1].islower() or word == "":
            word = random.choice(list(markovList))
            if "!m" not in word and "<end>" not in word and "@" not in word:
                continue
            else:
                word = ""
    else:
        word = startword
    
    chain = []
    del markovList["!mk"]
    del markovList["!markov"]
    if length > 1:
        while len(chain) < length:
            chain = [word]
            newword = random.choice(markovList[word])
            while len(chain) < length:
                try:
                    chain.append(newword)
                    newword = random.choice(markovList[newword])
                except:
                    continue
    else:
        randomLen = random.randint(1,14)
        while len(chain) < randomLen:
            chain = [word]
            newword = random.choice(markovList[word])
            while len(chain) < randomLen:
                try:
                    chain.append(newword)
                    newword = random.choice(markovList[newword])
                except:
                    continue
    returnChain = " ".join(chain)
    return returnChain

def makeMarkov(string, startword, user, mlength):
    passage = string.split()
    mList1 = makeMarkovList(passage)
    mChain1 = makeMarkovChain(mList1, startword, mlength)
    return mChain1
    #return 

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
    embed.add_field(name="-h, --history [INT]", value="Search history in No. of messages (def: 3000, max:50000)", inline=True)
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
        mlength = 0
        hlength = 3000
        splitMessage = message.content.split()
        for index, i in enumerate(splitMessage):
            if i == "-s" or i == "--startswith":
                startswith = splitMessage[index+1]
            elif index == 1 and "-" not in i:
                user = i
            elif i == "-l" or i == "--length":
                mlength = int(splitMessage[index+1])
            elif i == "-h" or i == "--history":
                hlength = int(splitMessage[index+1]) 
        
        if user != "":
            messmember = getUser(message, user)
        else:
            messmember = message.author
        print ("$:makeMarkov -u " + messmember.display_name + " -s " + startswith + " -l " + str(mlength) + " -h " + str(hlength))

        if hlength > 50000:
            hlength = 50000
        if mlength > 100:
            mlength = 100

        list = ""
        async for item in message.channel.history(limit=hlength):
            if item.author == messmember:
                list += (str(item.content) + " <end> ")
        
        markovChain = makeMarkov (list, startswith, user, mlength)

        if markovChain != "":
            print ("Printed: " + str(markovChain))
            print ("")
            if messmember.display_name[0].islower():
                newnick = messmember.display_name[0:20] + " markov"
            elif messmember.display_name.isupper():
                newnick = messmember.display_name[0:20] + " MARKOV"
            else:
                newnick = messmember.display_name[0:20] + " Markov"
            me = message.guild.me
            await discord.Member.edit(me, nick=newnick)
            #markovChain = markovChain.replace("@", "")
            await message.channel.send(markovChain)
            await discord.Member.edit(me, nick="")

    elif ("markov" in str(message.content).lower()) and ("bitch" in str(message.content).lower() or "fuck you" in str(message.content).lower() or "shitty bot" in str(message.content).lower() or "kys" in str(message.content).lower() or "kill yourself" in str(message.content).lower() or "fuck off" in str(message.content).lower()):
        await message.channel.send("бля сука")
        
keep_alive()
token = os.environ.get("DISCORD_BOT_SECRET")
client.run(token)
