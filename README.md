# markov-bot
*A Discord bot designed for Repl.it. Generates new messages using Markov chains from user message history*


Designed to work on Repl.it, running with a Flask server.

Paste the private code for your Discord bot in the .env file directly. It should look like this:
```
DISCORD_BOT_SECRET=T1bAcYNlVgqOHnbT6PbCgqOH.yVzxJ.wMHZ-pb2HXESAeiv0mUcXXak5_M
```
## Commands
* !mv, !markov [USER]... [OPTION]...
  * Basic syntax
* -s, --startswith [STR]
  * Chain starting word
* -l, --length [INT]
  * Chain length - Random length between 1 - 14 by default, Max: 100
* -h, --history [INT]
  * Search history in No. of messages - set to 3000 by default
  
## Examples:
```
!markov -s Heiroglyph -h 5000
Generates a chain for you, beginning with word "Heiroglyph", and searching through 5,000 messages

!mk PaulAtreides --limit 15 -h 15000
Generates a chain for user "PaulAtreides", limiting the markov chain to 15 words, and searching through 15,000 messages.
```

This is an example of the bot constructing Markov chains, using paragraphs pasted out of the Fellowship of the Ring. This was cut short by the default chain length
![markov-bot test with LOTR paragraphs](https://raw.githubusercontent.com/whambulance/markov-bot/master/markovtest1.png)
